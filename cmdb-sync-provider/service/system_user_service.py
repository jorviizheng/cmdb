from __future__ import print_function

from tornado.gen import coroutine, Return
from tornado.escape import json_decode
from tornado.log import gen_log
from tornado.web import HTTPError

import sys
import copy

sys.path.append('.')
from service.base_service import BaseService
from utils.http_util import http_client


class SystemUserService(BaseService):

    def __init__(self, ansible_json, cookie):
        BaseService.__init__(self, ansible_json, cookie)
        self.get_user_cmd = 'cat /etc/passwd'

    @coroutine
    def get_user(self):
        ansible_service = yield self.get_ansible_service()
        ansible_url = 'http://%s/ansible/task' % ansible_service
        self.ansible_json['args'] = self.get_user_cmd
        self.ansible_json['module'] = 'shell'
        try:
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as err:
            raise err
        else:
            result = json_decode(response.body)

            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                    user_list = list()
                    for user in host['msg']:
                        print(user)
                        uid = int(user.split(':')[2])
                        user_name = user.split(':')[0]
                        login = user.split(':')[-1]
                        if uid >= 1000 and 'nologin' not in login:
                            print(user_name)
                            user_list.append(user_name)
                    host['msg'] = user_list

            raise Return(result)







