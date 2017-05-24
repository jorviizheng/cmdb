from __future__ import print_function

from tornado.web import RequestHandler
from tornado.options import options
from tornado.gen import coroutine
from datetime import datetime


class CheckHandler(RequestHandler):

    @coroutine
    def get(self):
        now_time = datetime.now()
        now_time = now_time.strftime(options.date_fmt)
        check_msg = {
            'service': 'cmdb-controller',
            'status': 200,
            'time': now_time
        }
        self.write(check_msg)






