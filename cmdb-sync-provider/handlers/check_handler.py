from __future__ import print_function

# from tornado.web import authenticated
from tornado.escape import json_encode, json_decode
from tornado.options import options
from tornado.gen import coroutine
from datetime import datetime

from operator import eq

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from wrapper.route import route,authenticated


@route('/api/sync/v1/status')
class CheckHandler(BaseHandler):

    @coroutine
    @authenticated
    def get(self):
        now_time = datetime.now()
        now_time = now_time.strftime(options.date_fmt)
        check_msg = {
            'service': 'cmdb-async-api',
            'status': 200,
            'time': now_time
        }
        self.write(check_msg)






