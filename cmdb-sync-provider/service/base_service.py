from tornado.gen import coroutine, Return
from tornado.options import options
from tornado.log import gen_log

import sys
sys.path.append('.')
from utils.zk_util import Zookeeper


class BaseService(object):

    def __init__(self, ansible_json, cookie):
        self.ansible_json = ansible_json
        self.cookie = cookie

    def return_json(self,code,msg):
        return_json = dict()
        return_json['status'] = code
        return_json['msg'] = msg
        return return_json

    @coroutine
    def get_ansible_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.ansible_node_path)
        if path_exist is False:
            raise Exception('Ansible Service  None')
        try:
            node = yield zk.get_node(options.ansible_node_path)
            ansible_server = node[0].decode('utf8')
        except Exception as error:
            gen_log.error(error)
        else:
            raise Return(ansible_server)

    @coroutine
    def get_provision_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.provision_node_path)
        if path_exist is False:
            raise Exception('ProvisionService  None')
        try:
            node = yield zk.get_node(options.provision_node_path)
            provision_service = node[0].decode('utf8')
        except Exception as error:
            gen_log.error(error)
        else:
            raise Return(provision_service)