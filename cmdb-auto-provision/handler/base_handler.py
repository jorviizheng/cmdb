# -*- coding: utf-8 -*-
from __future__ import print_function

from tornado.web import RequestHandler
from tornado.httpclient import HTTPError
from tornado.gen import coroutine, Return
from tornado.options import options
from tornado.log import gen_log
from concurrent.futures import ThreadPoolExecutor
from tornadis import TornadisException

import sys
sys.path.append('.')
from utils.api_redis import SyncRedisUtil, AsyncRedisUtil
from utils.http_util import http_cookie
from utils.zk_util import Zookeeper


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

    @coroutine
    def get_async_api_cookie(self):
        try:
            async_api_url = yield self.get_async_api_service()
        except HTTPError as err:
            raise err
        else:
            try:
                #从redis获取对应的cookie
                redis = AsyncRedisUtil(self.application.async_session_pool)
                cookie_exist = yield redis.keys(options.service_user)
                cookie = None
                #不存在cookie
                if cookie_exist == 0:
                    cookie = yield http_cookie(async_api_url)
                    yield redis.set(options.service_user, cookie)
                    yield redis.expire(options.service_user, options.session_expire_time)
                else:
                    cookie = yield redis.get(options.service_user)
            except TornadisException as err:
                raise err
            else:
                raise Return(cookie)


    #获取API地址
    @coroutine
    def get_async_api_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.async_api_node_path)
        if path_exist is False:
            raise Exception('Async Api Service  None')
        try:
            node = yield zk.get_node(options.async_api_node_path)
            async_api_url = 'http://' + node[0].decode('utf8')
        except Exception as error:
            gen_log.error(error)
        else:
            raise Return(async_api_url)


    #获取ansible 服务地址
    @coroutine
    def get_ansible_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.ansible_node_path)
        if path_exist is False:
            raise Exception('Ansible Service  None')
        try:
            node = yield zk.get_node(options.ansible_node_path)
            ansible_url = 'http://' + node[0].decode('utf8')
        except Exception as error:
            gen_log.error(error)
        else:
            raise Return(ansible_url)