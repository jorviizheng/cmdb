import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from utils.api_pgsql import AsyncPgsql


class TaskDal(AsyncPgsql):
    table_name = 'task'
    task_id = 'task_id'
    user_name = 'user_name'
    task_status_id = 'task_status_id'
    task_name = 'task_name'
    task_type = 'task_type'
    task_flag = 'task_flag'
    task_args = 'task_args'
    create_time = 'create_time'
    update_time = 'update_time'
    result = 'result'

    def return_field(self):
        return {
        'user_name' : 'user_name',
        'task_status_id' : 'task_status_id',
        'task_name' : 'task_name',
        'task_type':'task_type',
        'task_flag':'task_flag',
        'task_args':'task_args',
        'create_time':'create_time',
        'update_time':'update_time',
        'result':'result'
        }

    @coroutine
    def insert(self, add_dict):
        try:
            result = yield self._insert(self.table_name, add_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    @coroutine
    def delete(self, search_dict):
        try:
            result = yield self._delete(self.table_name,search_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    @coroutine
    def update(self, update_dict, search_dict):
        try:
            result = yield self._update(self.table_name,update_dict,search_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    @coroutine
    def select(self, col_dict, search_dict, limit_dict=None, order_dict=None):
        try:
            result = yield self._select(self.table_name, col_dict, search_dict,limit_dict,order_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)