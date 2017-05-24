from __future__ import print_function

from tornado.gen import coroutine, Return
from tornado.escape import json_decode
from tornado.log import gen_log
from tornado.web import HTTPError
import sys

sys.path.append('.')
from service.base_service import BaseService
from utils.api_redis import AsyncRedisUtil
from utils.http_util import http_client


class YumSourceService(BaseService):
    SOURCE_NAME = 'yum_source'
    GET_SOURCE_LIST_CMD = 'ls /etc/yum.repos.d/'

    def __init__(self, pool, ansible_json, cookie):
        self.redis = AsyncRedisUtil(pool)
        self.source_name = ansible_json['source_name']
        BaseService.__init__(self, ansible_json, cookie)

    @coroutine
    def check_installed_resource(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.GET_SOURCE_LIST_CMD
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as error:
            gen_log.info(error)
            raise error
        else:
            result = json_decode(response.body)

            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                    source_name = self.source_name + '.repo'
                    if source_name not in host['msg']:
                        host['status'] = 1
            raise Return(result)

    @coroutine
    def get_installed_resource_list(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.GET_SOURCE_LIST_CMD
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as error:
            gen_log.info(error)
            raise error
        else:
            result = json_decode(response.body)

            repo_list = list()
            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                    for source in host['msg']:
                        repo_list.append(source.split('.')[0])
                    host['msg'] = repo_list
            raise Return(result)

    @coroutine
    def get_available_source_list(self):
        source_list = list()
        try:
            source_exist = yield self.redis.keys(self.SOURCE_NAME)
            if source_exist > 0:
                yum_source = yield self.redis.get(self.SOURCE_NAME)
                for key in yum_source.keys():
                    source_list.append(key)
        except HTTPError as error:
            gen_log.error(error)
        else:
            raise Return(self.return_json(0, source_list))


class YumPackageService(BaseService):
    GET_SOURCE_LIST_CMD = 'yum list installed |grep '

    def __init__(self, ansible_json, cookie):
        self.package_name = ansible_json['package_name']
        BaseService.__init__(self, ansible_json, cookie)

    @coroutine
    def check_package_installed(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.GET_SOURCE_LIST_CMD + self.package_name
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as error:
            gen_log.info(error)
            raise error
        else:
            result = json_decode(response.body)
            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                    if self.package_name in host['msg'][0]:
                        package_info = dict()
                        package = host['msg'][0]
                        package_info['name'] = package.split()[0]
                        package_info['version'] = package.split()[1]
                        host['msg'] = package_info
                    else:
                        host['status'] = 1
            raise Return(result)














