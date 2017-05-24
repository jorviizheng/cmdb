from __future__ import print_function

import sys
import os
sys.path.append('.')
from tornado.escape import json_decode
from tornado.gen import Return, coroutine
from tornado.log import gen_log
from tornado.httpclient import HTTPError

from jinja2 import Template

from utils.http_util import http_client


class DhcpService(object):

    def __init__(self, cookie, async_api_url, ansible_url, server_ip, manager_ip, mac_address):
        self.cookie = cookie
        self.async_api_url = async_api_url
        self.ansible_url = ansible_url

        self.server_ip = server_ip
        self.manager_ip = manager_ip
        self.mac_address = mac_address

    @coroutine
    def update_dhcp_config(self):

        file_path = os.path.join(os.path.dirname(__file__), "../templates/dhcpd.conf.template")
        template_file = open(file_path)
        try:
            template_buffer = template_file.read()
        except FileNotFoundError as err:
            raise err
        finally:
            template_file.close()

        template = Template(template_buffer)
        try:
            dhcp_list = yield self.get_dhcp_servers()
            pxe_template_list = yield self.get_pxe_templates()
        except HTTPError as err:
            raise err
        dhcp_tempalte = template.render(dhcp_servers=dhcp_list, pxe_template_list=pxe_template_list)
        dhcp_host = dhcp_list[0]['dhcp_server_ip']
        dhcp_dest = dhcp_list[0]['dhcp_config_path']
        try:
            url = self.ansible_url + '/ansible/task'
            dhcp_template_ansible_json = {
                'module': 'copy',
                'file_name': 'dhcpd.conf',
                'host': dhcp_host,
                'content': dhcp_tempalte,
                'dest': dhcp_dest
            }
            restart_dhcp_service_json  = {
            'module': 'systemd',
            'name': 'dhcpd',
            'state': 'restarted',
            'host': dhcp_host
            }

            yield http_client(url, 'POST', self.cookie, dhcp_template_ansible_json,60)

            yield http_client(url, 'POST', self.cookie, restart_dhcp_service_json,60)

        except HTTPError as err:
            raise err

    @coroutine
    def get_pxe_templates(self):
        url = '%s/api/async/v1/pxe/templates' % self.async_api_url
        try:
            response = yield http_client(url, 'GET', self.cookie)
        except HTTPError as error:
            gen_log.error('Get DHCP Template Error:%s' % error)
            raise error
        else:
            result = json_decode(response.body)
            gen_log.info(result)
            raise Return(result['msg'])

    @coroutine
    def get_dhcp_servers(self):
        url = '%s/api/async/v1/dhcp/servers' % self.async_api_url
        try:
            response = yield http_client(url, 'GET', self.cookie)
        except HTTPError as error:
            gen_log.error('Get DHCP Template Error:%s' % error)
            raise error
        else:
            result = json_decode(response.body)
            gen_log.info(result)
            raise Return(result['msg'])






