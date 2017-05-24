import sys
sys.path.append('.')
from tornado.gen import coroutine,Return
from utils.api_pgsql import AsyncPgsql


class DhcpServerDal(AsyncPgsql):
    #dhcp server
    table_name = 'dhcp_server'
    dhcp_server_id = 'dhcp_server_id'
    dhcp_subnet = 'dhcp_subnet'
    dhcp_netmask = 'dhcp_netmask'
    dhcp_routers = 'dhcp_routers'
    dhcp_domain_name = 'dhcp_domain_name'
    dhcp_domain_name_servers = 'dhcp_domain_name_servers'
    dhcp_next_server = 'dhcp_next_server'
    dhcp_server_ip = 'dhcp_server_ip'
    dhcp_range = 'dhcp_range'
    dhcp_range_start = 'dhcp_range_start'
    dhcp_range_end = 'dhcp_range_end'
    dhcp_config_path = 'dhcp_config_path'



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