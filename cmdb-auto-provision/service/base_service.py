from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine
from tornado.log import gen_log
from tornado.httpclient import HTTPError

from utils.ilo4_util import Ilo4Util
from service.dhcp_service import DhcpService


class BaseService(object):

    def __init__(self, cookie, api_url, ansible_url, init_json=dict()):

        self.server_name = init_json['server_name']
        self.manager_ip = init_json['manager_ip']
        self.server_ip = init_json['server_ip']
        self.mac_address = init_json['mac_address']
        self.ilo_user = init_json['ilo4_user_name']
        self.ilo4_passwd = init_json['ilo4_user_passwd']

        self.ansible_url = ansible_url
        self.async_api_url = api_url

        self.cookie = cookie

    @coroutine
    def install_server(self):

        ilo_client = Ilo4Util(self.manager_ip, self.ilo_user, self.ilo4_passwd)

        dhcp = DhcpService(self.cookie,
                           self.async_api_url,
                           self.ansible_url,
                           self.server_ip,
                           self.manager_ip,
                           self.mac_address)

        #更新dhcp 模板
        try:
            gen_log.info('Update DHCP Template')
            yield dhcp.update_dhcp_config()
        except Exception as err:
            raise Exception('Update Dhcp Template Error:%s' % err.args)

        #设置服务器网络启动
        try:
            gen_log.info('修改服务器%s临时启动顺序' % self.server_name)
            yield ilo_client.change_boot_temporary()
        except HTTPError as err:
            raise err

        #重启服务器
        try:
            gen_log.info('Reset Server: %s' % self.server_name)
            yield ilo_client.reset_server()
        except HTTPError as err:
            raise err

    def return_json(self,code, msg):
        return_json = dict()
        return_json['status'] = code
        return_json['msg'] = msg
        return return_json








