# -*- coding: utf-8 -*- 
from __future__ import print_function
import sys
sys.path.append('.')
from model.task_model import TaskModel
from model import task_status_model
from handlers.base_handler import BaseHandler
from wrapper.route import route, authenticated

from tornado.gen import coroutine
from tornado.escape import json_decode, json_encode

NEW_TASK_STATUS_ID = 1

@route('/api/async/v1/tasks')
class TaskHandler(BaseHandler):


    #获取task列表
    @coroutine
    @authenticated
    def get(self):
        limit_dict = {
            'start': self.get_argument('start', 'all'),
            'length': self.get_argument('length', 0)
        }

        order_colume_str = 'columns[%s][data]' % self.get_argument('order[0][column]',0)
        order_colume = self.get_argument(order_colume_str,None)
        sort_dict = {
            'order_colume': order_colume,
            'order_type': self.get_argument('order[0][dir]', 'acs')
        }

        task = TaskModel()
        total_lines = yield task.get_task_total()
        data_list = yield task.get_task(limit_dict, sort_dict)
        result_json = dict()
        result_json['draw'] = self.get_argument('draw')
        result_json['recordsTotal'] = total_lines
        result_json['recordsFiltered'] = total_lines

        if isinstance(data_list, int):
            self.write(result_json)
        elif isinstance(data_list,list):
            for item in data_list:
                task_status = task_status_model.TaskStatusModel()
                task_status.task_status_id = item['task_status_id']
                item['task_status_id'] = yield task_status.get_task_name_by_id()
            result_json['data'] = data_list
            self.write(result_json)

     #新增task
    @coroutine
    @authenticated
    def post(self):
        try:
            task = TaskModel()
            task_json = json_decode(self.request.body)
            task.user_name = task_json['user_name']
            task.task_status_id = NEW_TASK_STATUS_ID
            task.task_name = task_json['task_name']
            task.task_type = task_json['task_type']
            task.task_flag = task_json['task_flag']
            task.task_args = task_json['task_args']
            task.result = None
            task.create_time = task_json['create_time']
            task.update_time = task_json['update_time']
            result = yield task.add_task()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            if result == -1:
                self.write(self.return_json(-1, 'Error'))
            elif result == 0:
                self.write(self.return_json(0, 'Task Already Exist'))
            elif result > 0:
                self.write(self.return_json(1, 'Task Add'))

    #更新task
    @coroutine
    @authenticated
    def patch(self):
        task = TaskModel()
        task_json = json_decode(self.request.body)
        task.task_status_id = task_json['task_status_id']
        task.update_time = task_json['update_time']
        task.result = json_encode(task_json['result'])
        task.task_name = task_json['task_name']
        try:
            result = yield task.update_task()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(result, 'Done'))

    #删除task
    @coroutine
    @authenticated
    def delete(self):
        pass


@route('/api/async/v1/tasks/list/(.*)')
class GetTaskList(BaseHandler):
    @coroutine
    @authenticated
    def get(self, task_stauts_id):
        task = TaskModel()
        task.task_status_id = task_stauts_id
        try:
            tasks = yield task.get_task_by_status()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, tasks))


@route('/api/async/v1/tasks/count')
class GetTaskCount(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        task = TaskModel()
        try:
            result = yield task.get_tasks_count()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))