from __future__ import print_function
from tornado.httpclient import HTTPError
from tornado.gen import coroutine, Return, sleep
from tornado.options import options
from tornado.locale import gen_log
from tornado.escape import json_decode
from operator import eq

from tornadis import TornadisException

import sys
sys.path.append('.')
from service.server_service import ServerService
from service.ansible_service import AnsibleService
from utils.zk_util import Zookeeper
from utils.api_redis import AsyncRedisUtil
from utils.http_util import http_cookie, http_client

TASK_STATUS_NEW_ID = 1
TASK_STATUS_WAIT_CHECK = 6


class TaskHandler(object):

    def __init__(self, queue, pool):
        self.queue = queue
        self.async_api_url = ''
        self.pool = pool

    @coroutine
    def get_async_api_cookie(self):
        try:
            async_api_url = yield self.get_async_api_service()
        except HTTPError as err:
            raise err
        else:
            try:
                #从redis获取对应的cookie
                redis = AsyncRedisUtil(self.pool)
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

    @coroutine
    def new_task(self):
        async_api_url = yield self.get_async_api_service()
        if async_api_url:
            cookie = yield self.get_async_api_cookie()
            try:
                yield self.get_new_task(async_api_url, cookie)
            except HTTPError as err:
                gen_log.error(err.args)

    @coroutine
    def check_task(self):
        async_api_url = yield self.get_async_api_service()
        if async_api_url:
            cookie = yield self.get_async_api_cookie()
            try:
                yield self.get_waitting_check_task(async_api_url, cookie)
            except HTTPError as err:
                gen_log.error(err.args)

    #获取task
    @coroutine
    def get_tasks(self, fetch_url, cookie):
        try:
            response = yield http_client(fetch_url, 'GET', cookie)
        except HTTPError as err:
            raise err
        else:
            tasks = json_decode(response.body)
            # print(tasks)
            try:
                yield self.queue.put(tasks)
            except Exception as e:
                gen_log.error(e)

    #获取新建状态task
    @coroutine
    def get_new_task(self, async_api_url, cookie):
        fetch_url = '%s/api/async/v1/tasks/list/%s' % (async_api_url, TASK_STATUS_NEW_ID)
        try:
            yield self.get_tasks(fetch_url, cookie)
        except HTTPError as err:
            raise err


    #获取待检测的任务
    @coroutine
    def get_waitting_check_task(self, async_api_url, cookie):
        fetch_url = '%s/api/async/v1/tasks/list/%s' % (async_api_url, TASK_STATUS_WAIT_CHECK)
        try:
            yield self.get_tasks(fetch_url, cookie)
        except HTTPError as err:
            raise err

    @coroutine
    def consumer(self):
        try:
            task_json = yield self.queue.get()
            if task_json['status'] == 0:
                async_api_url = yield self.get_async_api_service()
                cookie = yield self.get_async_api_cookie()
                if task_json['msg'] != 0:
                    for tasks in task_json['msg']:
                        task_status_id = tasks['task_status_id']
                        task_flag = json_decode(tasks['task_flag'])
                        task_type = task_flag['type']
                        if eq(task_type, 'server'):
                            server = ServerService(cookie, async_api_url, tasks, task_flag['action'])
                            if task_status_id == TASK_STATUS_NEW_ID:
                                yield server.provision()
                            elif task_status_id == TASK_STATUS_WAIT_CHECK:
                                yield server.check_server_install_result()
                        elif eq(task_type, 'ansible'):
                            ansible = AnsibleService(cookie, async_api_url, tasks)
                            yield ansible.run_ansible_task()
        except Exception as err:
            gen_log.error(err)
            raise err
        finally:
            self.queue.task_done()




