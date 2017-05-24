import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from utils.api_pgsql import AsyncPgsql


class KickstartsDal(AsyncPgsql):
    #cobbler profile
    table_name = 'kickstarts'
    ksp_id = 'ksp_id'
    kickstarts_profile_path = 'kickstarts_profile_path'
    kickstarts_profile_name = 'kickstarts_profile_name'


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
