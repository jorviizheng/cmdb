import sys
sys.path.append('.')
from tornado.gen import coroutine,Return
from utils.api_pgsql import AsyncPgsql


class ServiceStatusDal(AsyncPgsql):
    table_name = 'service_status'
    service_status_id = 'service_status_id'
    service_id = 'service_id'
    server_id = 'server_id'
    create_date = 'create_date'
    last_excute_time = 'last_excute_time'

    def return_field(self):
        return {
        'service_id' : 'service_id',
        'server_id':'server_id',
        'create_date':'create_date',
        'last_excute_time':'last_excute_time'
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
    


