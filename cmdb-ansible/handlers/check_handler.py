from __future__ import print_function

from tornado.options import options
from tornado.gen import coroutine
from datetime import datetime

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from wrapper.route import route

@route('/ansible/status')
class CheckHandler(BaseHandler):

    @coroutine
    def get(self):
        now_time = datetime.now()
        now_time = now_time.strftime(options.date_fmt)
        print(self.request.headers)
        print(self.get_secure_cookie('user-key'))
        check_msg = {
            'service': 'cmdb-ansible',
            'status': 200,
            'time': now_time,
            'cookie': self.cookies
        }
        self.write(check_msg)






