from __future__ import print_function
from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.httpclient import HTTPError
from tornado.log import gen_log
import re
from operator import eq


import sys
sys.path.append('.')
from service.base_service import BaseService
from wrapper.permisson_wrapper import permisson
from utils.http_util import http_client


class AnsibleService(BaseService):

    def __init__(self, cookie, async_api_url, init_json):
        BaseService.__init__(self, cookie, async_api_url, init_json)
        self.ansible_json = self.task_args

    @coroutine
    @permisson
    def run_ansible_task(self):
        gen_log.info('Task %s Start' % self.task_name)
        try:
            # 更新任务状态
            try:
                yield self.update_task_handler()
            except Exception as err:
                raise err

            # 获取ansible service
            ansible_url = ''
            try:
                ansible_service = yield self.get_ansible_service()
                ansible_url = 'http://%s/%s' % (ansible_service, 'ansible/task')

            except Exception as err:
                gen_log.error(err.args)
                raise Exception('Get Ansible Service Error')

            # 执行ansible任务
            try:
                response = yield http_client(ansible_url, 'POST', None, self.ansible_json, 60)
            except HTTPError as err:
                gen_log.error('Run Ansible %s %s Error:%s' % (self.task_name, ansible_url, err.args))
                self.result = self.return_json(-1, err.message)
                yield self.update_task_fail()
            else:
                result = json_decode(response.body)
                self.result = result
                try:
                    if eq(result['status'], 0):
                        yield self.update_task_success()
                    else:
                        yield self.update_task_fail()
                except HTTPError as err:
                    raise err

        except Exception as err:
            self.result = self.return_json(-1, err.args)
            yield self.update_task_fail()

