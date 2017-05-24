import sys
sys.path.append('.')
from tornado.gen import coroutine,Return
from utils.api_pgsql import AsyncPgsql


class GroupDal(AsyncPgsql):
    table_name = 'user_group'
    gid = 'gid'
    group_name = 'group_name'
    uid_list = 'uid_list'
    pid = 'pid'

    def return_field(self):
        return {
        'group_name' : 'group_name',
        'uid_list' : 'uid_list',
        'pid' : 'pid'
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


