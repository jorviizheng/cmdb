import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from utils.api_pgsql import AsyncPgsql


class DhcpMapDal(AsyncPgsql):
    #dhcp map table
    table_name = 'dhcp_map'
    server_id = 'server_id'
    dhcp_map_id = 'dhcp_map_id'
    server_ip = 'server_ip'
    manager_ip = 'manager_ip'
    mac_address = 'mac_address'

    @coroutine
    def get_table_field(self):
        fields = yield self._get_table_rows(self.table_name)
        raise Return(fields)


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