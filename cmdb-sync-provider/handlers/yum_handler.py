from __future__ import print_function

from tornado.web import asynchronous,HTTPError
from tornado.escape import json_decode
from tornado.concurrent import run_on_executor
from tornado.log import gen_log
from tornado.gen import coroutine

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from service.yum_service import YumSourceService,YumPackageService
from wrapper.route import route,authenticated
from utils.api_redis import AsyncRedisUtil



SOURCE_NAME = 'yum_source'


@route('/api/sync/v1/yum/source/available')
class GetAvailableYumSource(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        yum_source = dict()
        redis = AsyncRedisUtil(self.application.yum_source_pool)
        try:
            source_exist = yield redis.keys(SOURCE_NAME)
            if source_exist > 0:
                yum_source = yield redis.get(SOURCE_NAME)
        except HTTPError as error:
            gen_log.error(error)
            self.write(self.return_json(-1,error.args))
        else:
            self.write(self.return_json(0, yum_source))


@route('/api/sync/v1/yum/source/installed')
class GetInstalledYumSource(BaseHandler):
    @run_on_executor
    @asynchronous
    @coroutine
    @authenticated
    def post(self):
        ansible_json = json_decode(self.request.body)
        cookie = self.request.headers['Cookie']
        try:
            yys = YumSourceService(self.application.server_pool, ansible_json, cookie)
            result = yield yys.check_installed_resource()
        except HTTPError as error:
            gen_log.error(error)
            self.write(self.return_json(-1, error.args))
        else:
            self.write(result)


@route('/api/sync/v1/yum/source/installed/list')
class GetInstalledYumSourceList(BaseHandler):
    @run_on_executor
    @asynchronous
    @coroutine
    @authenticated
    def post(self):
        ansible_json = json_decode(self.request.body)
        cookie = self.request.headers['Cookie']
        try:
            yys = YumSourceService(self.application.server_pool, ansible_json, cookie)
            result = yield yys.get_installed_resource_list()
        except HTTPError as error:
            gen_log.error(error)
            self.write(self.return_json(-1, error.args))
        else:
            self.write(result)


@route('/api/sync/v1/yum/package/installed')
class GetInstalledPackage(BaseHandler):
    @run_on_executor
    @asynchronous
    @coroutine
    @authenticated
    def post(self):
        ansible_json = json_decode(self.request.body)
        cookie = self.request.headers['Cookie']
        try:
            yps = YumPackageService(ansible_json, cookie)
            result = yield yps.check_package_installed()
        except HTTPError as error:
            self.write(self.return_json(-1,error.args))
        else:
            self.write(result)
