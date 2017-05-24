import sys
sys.path.append('.')
from tornado.gen import coroutine,Return
from utils.api_pgsql import AsyncPgsql


class ServiceDal(AsyncPgsql):
    table_name = 'service'
    service_id = 'service_id'
    service_type = 'service_type'
    service_name = 'service_name'
    service_version = 'service_version'

    def return_field(self):
        return {
        'service_type' : 'service_type',
        'service_name' : 'service_name',
        'service_version' : 'service_version'
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