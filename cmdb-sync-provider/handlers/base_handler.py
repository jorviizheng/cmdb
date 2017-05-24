# -*- coding: utf-8 -*-
from __future__ import print_function

from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.append('.')
from utils.api_redis import SyncRedisUtil



class BaseHandler(RequestHandler):
    executor = ThreadPoolExecutor(30)

    def return_json(self,code,msg):
        return_json = dict()
        return_json['status'] = code
        return_json['msg'] = msg
        return return_json

    def get_current_user(self):
        cookie_id = self.get_cookie('user-key')
        redis = SyncRedisUtil(self.application.sync_session_pool)
        if redis.key_exist(cookie_id):
            return cookie_id
        return None
