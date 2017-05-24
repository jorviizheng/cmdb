import sys
sys.path.append('.')
from tornado.gen import coroutine,Return
from utils.api_pgsql import AsyncPgsql


class ServerDal(AsyncPgsql):

    table_name = 'server'
    server_id = 'server_id'
    idc_id = 'idc_id'
    pt_id = 'pt_id'
    dhcp_server_id = 'dhcp_server_id'
    server_name = 'server_name'
    root_password = 'root_password'
    manager_ip = 'manager_ip'
    server_ip = 'server_ip'
    server_group = 'server_group'
    server_type = 'server_type'
    system_type = 'system_type'
    tag = 'tag'
    status = 'status'
    machine_type = 'machine_type'    
    sn = 'sn'
    cpu = 'cpu'
    memory = 'memory'
    hardisk = 'hardisk'
    raid = 'raid'
    rack_type = 'rack_type'

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
    def select(self, col_dict, search_dict, limit_dict=None, order_dict=None):
        try:
            result = yield self._select(self.table_name, col_dict, search_dict,limit_dict,order_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)