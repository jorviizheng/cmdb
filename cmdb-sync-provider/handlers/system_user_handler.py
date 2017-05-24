from __future__ import print_function

from tornado.web import HTTPError, asynchronous
from tornado.escape import json_decode
from tornado.concurrent import run_on_executor
from tornado.log import gen_log
from tornado.gen import coroutine

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from service.system_user_service import SystemUserService
from wrapper.route import route,authenticated


@route('/api/sync/v1/system/users')
class GetSystemUsers(BaseHandler):
    @coroutine
    @authenticated
    def post(self):
        ansible_json = json_decode(self.request.body)
        cookie = self.request.headers['Cookie']
        sus = SystemUserService(ansible_json, cookie)
        try:
            result = yield sus.get_user()
        except HTTPError as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

