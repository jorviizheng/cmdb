# -*- coding: utf-8 -*-
from __future__ import print_function
from tornado.gen import coroutine, Return
from tornado.escape import json_decode

from operator import eq


import sys
sys.path.append('.')

from model.dhcp_server_model import DhcpServerModel
from model.dhcp_map_model import DhcpMapModel
from model.pxe_template_model import PxeTemplateModel
from handlers.base_handler import BaseHandler
from wrapper.route import route, authenticated


@route('/api/async/v1/dhcp/server/(.*)')
class DhcpServerHandler(BaseHandler):

    @coroutine
    @authenticated
    def get(self, dhcp_server_id):
        dm = DhcpServerModel()
        dm.dhcp_server_id = dhcp_server_id
        try:
            dhcp_server_ip = yield dm.get_dhcp_server_ip_by_id()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, dhcp_server_ip))

@route('/api/async/v1/dhcp/servers')
class DhcpServerListHandler(BaseHandler):

    @coroutine
    @authenticated
    def get(self):
        dm = DhcpServerModel()
        try:
            dhcp_list = yield dm.get_dhcp_server_list()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, dhcp_list))

#获取dhcp 可用IP
@route('/api/async/v1/dhcp/range/(.*)')
class DhcpRangeHandler(BaseHandler):
    @coroutine
    def get(self, dhcp_server_id):
        dm = DhcpServerModel()
        dm.dhcp_server_id = dhcp_server_id
        dhcp_range_ip = yield dm.get_dhcp_range_by_id()

        dmm = DhcpMapModel()
        dhcp_list = yield dmm.get_dhcp_list()
        if dhcp_list:
            for item in dhcp_list:
                if item['server_ip'] in dhcp_range_ip:
                    dhcp_range_ip.remove(item['server_ip'])

        self.write(self.return_json(0, dhcp_range_ip))



# #对dhcp map进行查询，新增，更新
@route('/api/async/v1/dhcp/map')
class DhcpMapHandler(BaseHandler):

    #查询
    @coroutine
    @authenticated
    def get(self):
        dmm = DhcpMapModel()
        dmm.mac_address = self.get_argument('mac_addr')
        try:
            dhcp_map = yield dmm.get_dhcp_map_by_mac_addr()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, dhcp_map))

    #更新map
    @coroutine
    @authenticated
    def post(self):
        dmm = DhcpMapModel()
        dhcp_json = json_decode(self.request.body)

        table_cols = yield dmm.dal.get_table_field()
        update_keys = self.get_row_dict(dhcp_json, table_cols)

        update_dict = dict()
        for key in update_keys:
            update_dict[key] = dhcp_json[key]

        search_dict = {
            dmm.dal.mac_address: update_dict['mac_address']
        }

        dmm.mac_address = update_dict['mac_address']
        mac_exist = yield dmm.check_mac_exist()
        try:
            if mac_exist == 0:
                result = yield dmm.add_new_dhcp(update_dict)
            else:
                result = yield dmm.update_dhcp(update_dict, search_dict)
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))


#获取pxe template 列表
@route('/api/async/v1/pxe/templates')
class GetPxeTemplates(BaseHandler):

    @coroutine
    def get(self):
        pt = PxeTemplateModel()
        try:
            result = yield pt.get_pxe_templates()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))

#获取pxe template 列表
@route('/api/async/v1/pxe/names')
class GetPxeList(BaseHandler):

    @coroutine
    def get(self):
        pt = PxeTemplateModel()
        try:
            result = yield pt.get_pxe_template_name_list()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))