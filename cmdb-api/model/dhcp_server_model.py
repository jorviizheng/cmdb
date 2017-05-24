import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal.dhcp_server_dal import DhcpServerDal


class DhcpServerModel(object):

    def __init__(self):
        self.dal = DhcpServerDal()
        self.dhcp_server_id = 1
        self.dhcp_subnet = ''
        self.dhcp_netmask = ''
        self.dhcp_routers = ''
        self.dhcp_domain_name = ''
        self.dhcp_domain_name_servers = ''
        self.dhcp_server_ip = ''
        self.dhcp_range = ''
        self.dhcp_range_start = 100
        self.dhcp_range_end = 254
        self.dhcp_config_path = ''

    @coroutine
    def get_dhcp_server_ip_by_id(self):
        col_dict = {
            self.dal.dhcp_server_ip: self.dal.dhcp_server_ip
        }
        search_dict = {
            self.dal.dhcp_server_id: self.dhcp_server_id
        }
        try:
            result = yield self.dal.select(col_dict, search_dict)
        except Exception as err:
            raise err
        else:
            if result != 0:
                result = result[0][self.dal.dhcp_server_ip]
            raise Return(result)

    @coroutine
    def get_dhcp_range_by_id(self):
        search_dict = {
            self.dal.dhcp_server_id: self.dhcp_server_id
        }
        try:
            result = yield self.dal.select('*', search_dict)
        except Exception as err:
            raise err
        else:
            if result != 0:
                result = result[0]
            range_ip_list = []
            for index in range(result[self.dal.dhcp_range_start], result[self.dal.dhcp_range_end]+1):
                range_ip_list.append('%s.%s' % (result[self.dal.dhcp_range],index))
            raise Return(range_ip_list)

    @coroutine
    def get_dhcp_server_list(self):
        try:
            result = yield self.dal.select('*', None)
        except Exception as err:
            raise err
        else:
            raise Return(result)
