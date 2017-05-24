# -*- coding: utf-8 -*- 
from __future__ import print_function

from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.append('.')
from utils.api_redis import SyncRedisUtil

class BaseHandler(RequestHandler):
    executor = ThreadPoolExecutor(30)

    def write(self, chunk):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Credentials', 'True')
        self.set_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        super(BaseHandler, self).write(chunk)

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

    #获取需要更新的数据库字段
    def get_row_dict(self, row_dict, allowed_keys):
        keys = allowed_keys.intersection(row_dict)
        return keys