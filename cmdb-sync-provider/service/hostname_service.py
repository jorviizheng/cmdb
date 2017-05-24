from __future__ import print_function

from tornado.gen import coroutine, Return
from tornado.escape import json_decode
from tornado.log import gen_log
from tornado.web import HTTPError

import sys

sys.path.append('.')
from service.base_service import BaseService
from utils.http_util import http_client


class HostnameService(BaseService):

    def __init__(self, ansible_json, cookie):
        BaseService.__init__(self, ansible_json, cookie)
        self.get_hostname_cmd = 'hostname'

    @coroutine
    def get_hostname(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.get_hostname_cmd
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as err:
            gen_log.info(err)
            raise err
        else:
            raise Return(response.body)

















