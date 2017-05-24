from __future__ import print_function

import sys

sys.path.append('.')

from tornado.escape import json_decode
from tornado.gen import coroutine, sleep
from tornado.httpclient import HTTPError
from tornado.log import gen_log
from operator import eq

from service.base_service import BaseService
from utils.http_util import http_client


class ServerService(BaseService):

    def __init__(self, cookie, async_api_url, init_json, action):
        BaseService.__init__(self, cookie, async_api_url, init_json)
        self.action = action

    @coroutine
    def provision(self):
        try:
            # 更新任务状态
            try:
                yield self.update_task_handler()
            except Exception as err:
                raise err
            # 获取自动装机服务
            try:
                provision_service = yield self.get_provision_service()
            except Exception as err:
                gen_log.error('Get Provision Service Error From Zookeeper:%s' % err.args)
                raise Exception('Get Provision Service Error From Zookeeper')

            provision_url = provision_service + '/provision/v1/server'

            result = self.return_json(3, 'Unknown Status')

            if eq(self.action, 'add'):
                # 新装服务器
                try:
                    response = yield http_client(provision_url, 'POST', self.cookie, self.task_args, 15)
                except HTTPError as err:
                    gen_log.error(err.message)
                    raise err
                else:
                    result = json_decode(response.body)
            elif eq(self.action, 'reinstall'):
                # 重装服务器
                try:
                    response = yield http_client(provision_url, 'PUT', self.cookie, self.task_args, 15)
                except HTTPError as err:
                    gen_log.error(err.message)
                    raise err
                else:
                    result = json_decode(response.body)
            self.result = result
            if result['status'] == 0:
                yield self.update_task_wait_check()
            elif result['status'] == -1:
                yield self.update_task_fail()
        except HTTPError as err:
            self.result = self.return_json(-1, err.message)
            yield self.update_task_fail()
        except Exception as err:
            self.result = self.return_json(-1, err.args)
            yield self.update_task_fail()

    @coroutine
    def check_server_install_result(self):

        try:
            # 更新任务状态为检测中
            try:
                yield self.update_task_checking()
            except Exception as err:
                raise err

            # 获取自动装机服务
            try:
                provision_service = yield self.get_provision_service()
            except Exception as err:
                gen_log.error('Get Provision Service Error From Zookeeper:%s' % err.args)
                raise Exception('Get Provision Service Error From Zookeeper')

            # 检测服务器安装状态
            # 每分钟检测一次，检测20次
            gen_log.info('每60S检测一次任务-%s-安装结果，总共检测20次' % self.task_name)
            times = 21
            success = False
            index = 1

            provision_url = provision_service + '/provision/v1/server/check?server_ip=%s' % self.task_args['server_ip']
            result = self.return_json(3, 'Unknown Status')
            while True:
                if index < times:
                    response = yield http_client(provision_url, 'GET', self.cookie)
                    result = json_decode(response.body)
                    if result['status'] == -1:
                        gen_log.info('第%s次检测, 服务器%s检测不成功，未达到次数限制，等待60S' % (index, self.task_name))
                        yield sleep(60)
                    else:
                        gen_log.info('服务器%s安装完成' % self.task_name)
                        success = True
                        break
                else:
                    gen_log.info('服务器%s安装失败' % self.task_name)
                    break
                index += 1

            if success:
                # 更新server信息
                yield self.update_server()

                if self.action == 'reinstall':
                    self.result = self.return_json(0, '%s reinstall success' % self.task_args['server_name'])
                elif self.action == 'add':
                    self.result = self.return_json(0, '%s install success' % self.task_args['server_name'])

                yield self.update_task_success()
            else:
                self.result = self.return_json(-1, '%s install fail' % self.task_args['server_name'])
                yield self.update_task_fail()
        except Exception as err:
            self.result = self.return_json(-1, err.args)
            yield self.update_task_fail()

    #更新db信息
    @coroutine
    def update_server(self):
        update_json = {
            'manager_ip': self.task_args['manager_ip'],
            'status': '运行正常',
        }
        url = self.async_api_url + '/api/async/v1/servers'
        try:
            yield http_client(url, 'PATCH', self.cookie, update_json)
        except HTTPError as err:
            self.result = self.return_json(-1, err.message)
            yield self.update_task_fail()







