from __future__ import print_function

from tornado.web import HTTPError
from tornado.escape import json_decode
from tornado.concurrent import run_on_executor
from tornado.log import gen_log
from tornado.gen import coroutine

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from service.hostname_service import HostnameService
from wrapper.route import route,authenticated


@route('/api/sync/v1/hostname')
class GetHostnameHandler(BaseHandler):
    @coroutine
    @authenticated
    def post(self):
        ansible_json = json_decode(self.request.body)
        cookie = self.request.headers['Cookie']
        host_name = HostnameService(ansible_json, cookie)
        try:
            result = yield host_name.get_hostname()
        except HTTPError as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)
