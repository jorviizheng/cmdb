import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from utils.api_pgsql import AsyncPgsql


class TaskStatusDal(AsyncPgsql):
    table_name = 'task_status'
    task_status_id = 'task_status_id'
    task_status_name = 'task_status_name'

    def return_field(self):
        return {
        'task_status_name' : 'task_status_name',
        }

    @coroutine
    def insert(self, add_dict):
        try:
            result = yield self._insert(self.table_name,add_dict)
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
    def select(self, col_dict, search_dict, limit_dict=None):
        try:
            result = yield self._select(self.table_name, col_dict, search_dict,limit_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)
    


