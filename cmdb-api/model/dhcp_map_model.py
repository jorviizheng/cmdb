import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal.dhcp_map_dal import DhcpMapDal


class DhcpMapModel(object):

    def __init__(self):
        self.dal = DhcpMapDal()
        self.dhcp_map_id = 1
        self.server_id = 1
        self.server_ip = ''
        self.manager_ip = ''
        self.mac_address = ''

    # def get_model_json(self):
    #     return {
    #         self.dal.server_id:self.server_id,
    #         self.dal.server_ip:self.server_ip,
    #         self.dal.manager_ip:self.manager_ip,
    #         self.dal.mac_address:self.mac_address
    #     }


    #检查macaddr是否已绑定过IP
    # 0  未绑定
    # 1  已绑定
    @coroutine
    def check_mac_exist(self):
        search_dict = {
            self.dal.mac_address: self.mac_address
        }
        result = yield self.dal.select('*', search_dict)
        if result == 0:
            raise Return(0)
        else:
            raise Return(1)

    #通过mac获取信息
    @coroutine
    def get_dhcp_map_by_mac_addr(self):
        search_dict = {
            self.dal.mac_address: self.mac_address
        }
        try:
            result = yield self.dal.select('*', search_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    #新增dhcp map 映射
    @coroutine
    def add_new_dhcp(self, add_dict):
        try:
            result = yield self.dal.insert(add_dict)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    @coroutine
    def update_dhcp(self, update_dict, search_dict):
        # update_dict = {
        #     self.dal.server_id: self.server_id,
        #     self.dal.server_ip: self.server_ip,
        #     self.dal.manager_ip: self.manager_ip,
        #     self.dal.mac_address: self.mac_address
        # }
        # search_dict = {
        #     self.dal.mac_address: self.mac_address
        # }
        try:
            result = yield self.dal.update(update_dict, search_dict)
            print(result)
        except Exception as err:
            raise err
        else:
            raise Return(result)

    @coroutine
    def get_dhcp_list(self):
        result = yield self.dal.select('*', None)
        raise Return(result)

