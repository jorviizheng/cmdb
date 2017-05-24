from __future__ import print_function

import sys

sys.path.append('.')

from datetime import datetime
from tornado.escape import json_decode
from tornado.gen import Return, coroutine
from tornado.log import gen_log
from tornado.options import options
from tornado.httpclient import HTTPError
from utils.http_util import http_client
from utils.zk_util import Zookeeper

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
TASK_STATUS_HANDLER_ID = 3
TASK_STATUS_SUCCESS_ID = 4
TASK_STATUS_FAILURE_ID = 5
TASK_STATUS_WAIT_CHECK = 6
TASK_STATUS_CHECKING = 7
TASK_URI = 'api/async/v1/tasks'


class BaseService(object):
    task_name = ''
    task_type = 'timely'
    task_status_id = 0
    task_flag = ''
    user_name = ''
    result = ''
    create_time = None
    update_time = None
    task_args = dict()

    cookie = None

    zk = None

    async_api_url = ''
    ansible_url = ''

    def __init__(self, cookie, async_api_url, init_json=dict()):
        self.task_name = init_json['task_name']
        self.create_time = init_json['create_time']
        self.update_time = init_json['update_time']
        self.user_name = init_json['user_name']
        self.result = init_json['result']
        self.task_type = init_json['task_type']
        self.task_flag = json_decode(init_json['task_flag'])
        self.task_args = json_decode(init_json['task_args'])
        self.zk = Zookeeper(options.zk_host)

        self.cookie = cookie
        self.async_api_url = async_api_url

    def return_json(self, status, msg):
        return_json = dict()
        return_json['status'] = status
        return_json['msg'] = msg
        return return_json

    @coroutine
    def update_task_handler(self):
        self.result = {
            'msg': '任务执行中'
        }
        post_json = {
            'task_status_id': TASK_STATUS_HANDLER_ID,
            'update_time': datetime.strftime(datetime.now(), DATETIME_FMT),
            'result': self.result,
            'task_name': self.task_name
        }
        url = '%s/%s' % (self.async_api_url, TASK_URI)
        try:
            response = yield http_client(url, 'PATCH', self.cookie, post_json)
        except HTTPError as err:
            gen_log.error('Update Task Handler %s Error:%s' % (self.task_name, err.message))
            raise err
        else:
            result = json_decode(response.body)

            if result['status'] < 0:
                gen_log.error('Update Task %s Handler:%s' % (self.task_name, result['msg']))
                raise Exception('Update Handler <%s> error: %s' % (self.task_name, result['msg']))
            else:
                gen_log.info('Update Task %s Handler: Done' % self.task_name)

    @coroutine
    def update_task_fail(self):
        post_json = {
            'task_status_id': TASK_STATUS_FAILURE_ID,
            'update_time': datetime.strftime(datetime.now(), DATETIME_FMT),
            'result': self.result,
            'task_name': self.task_name,
        }
        gen_log.info(post_json)
        url = '%s/%s' % (self.async_api_url, TASK_URI)
        try:
            response = yield http_client(url,'PATCH',self.cookie, post_json)
            gen_log.error(response.body)
        except HTTPError as err:
            gen_log.error('Update Task Fail %s Error:%s' % (self.task_name, err.message))
            raise err
        else:
            result = json_decode(response.body)
            print(result)
            if result['status'] < 0:
                gen_log.error('Update Task Fail %s Error' % self.task_name)
                raise Exception('Update Fail <%s> error: %s' % (self.task_name, result['msg']))
            else:
                gen_log.info('Update Task %s Fail: Done' % self.task_name)

    @coroutine
    def update_task_success(self):
        post_json = {
            'task_status_id': TASK_STATUS_SUCCESS_ID,
            'update_time': datetime.strftime(datetime.now(), DATETIME_FMT),
            'result': self.result,
            'task_name': self.task_name
        }
        url = '%s/%s' % (self.async_api_url, TASK_URI)
        try:
            response = yield http_client(url, 'PATCH', self.cookie, post_json)
        except HTTPError as err:
            gen_log.error('Update Task %s Success Error:%s' % (self.task_name, err.message))
            raise Exception('Update Task %s Success Error:%s' % (self.task_name, err.message))
        else:
            result = json_decode(response.body)
            if result['status'] < 0:
                gen_log.error('Task : %s ,Update Success:Error:%s' % (self.task_name, result['msg']))
                raise Exception('Update Success <%s> error: %s' % (self.task_name, result['msg']))
            else:
                gen_log.info('Task : %s ,Update Success:Done' % self.task_name)

    @coroutine
    def update_task_wait_check(self):
        post_json = {
            'task_status_id': TASK_STATUS_WAIT_CHECK,
            'update_time': datetime.strftime(datetime.now(), DATETIME_FMT),
            'result': self.result,
            'task_name': self.task_name
        }
        url = '%s/%s' % (self.async_api_url, TASK_URI)
        try:
            response = yield http_client(url, 'PATCH', self.cookie, post_json)
        except HTTPError as err:
            gen_log.error('Update Task %s Success Error:%s' % (self.task_name, err.message))
            raise Exception('Update Task %s Success Error:%s' % (self.task_name, err.message))
        else:
            result = json_decode(response.body)
            if result['status'] < 0:
                gen_log.error('Task : %s ,Update Wait Check:Error:%s' % (self.task_name, result['msg']))
                raise Exception('Update Wait Check <%s> error: %s' % (self.task_name, result['msg']))
            else:
                gen_log.info('Task : %s ,Update Wait Check:Done' % self.task_name)

    @coroutine
    def update_task_checking(self):
        post_json = {
            'task_status_id': TASK_STATUS_CHECKING,
            'update_time': datetime.strftime(datetime.now(), DATETIME_FMT),
            'result': self.result,
            'task_name': self.task_name
        }
        url = '%s/%s' % (self.async_api_url, TASK_URI)
        try:
            response = yield http_client(url, 'PATCH', self.cookie, post_json)
        except HTTPError as err:
            gen_log.error('Update Task %s Success Error:%s' % (self.task_name, err.message))
            raise Exception('Update Task %s Success Error:%s' % (self.task_name, err.message))

        else:
            result = json_decode(response.body)
            if result['status'] < 0:
                gen_log.error('Task : %s ,Update  Checking:Error:%s' % (self.task_name, result['msg']))
                raise Exception('Update Checking <%s> error: %s' % (self.task_name, result['msg']))
            else:
                gen_log.info('Task : %s ,Update Checking:Done' % self.task_name)


    @coroutine
    def get_ansible_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.ansible_node_path)
        if path_exist is False:
            raise Exception('Ansible Service  None')
        try:
            node = yield zk.get_node(options.ansible_node_path)
            ansible_url = node[0].decode('utf8')
        except Exception as err:
            raise err
        else:
            raise Return(ansible_url)

    @coroutine
    def get_provision_service(self):
        zk = Zookeeper(options.zk_host)
        path_exist = yield zk.check_path_exist(options.provision_node_path)
        if path_exist is False:
            raise Exception('Async Provision Service  None')
        try:
            node = yield zk.get_node(options.provision_node_path)
            provision_url = 'http://' + node[0].decode('utf8')
        except Exception as err:
            raise err
        else:
            raise Return(provision_url)








