# -*- coding: utf-8 -*- 
from __future__ import print_function

from tornado.gen import coroutine,Return
from tornado.escape import json_decode

import sys
sys.path.append('.')

from model.idc_model import IdcModel
from model.server_model import ServerModel
from handlers.base_handler import BaseHandler

from wrapper.route import route,authenticated


@route('/api/async/v1/servers')
class ServerHandler(BaseHandler):
    #获取服务器列表
    @coroutine
    def get(self):
        limit_dict = {
            'start': self.get_argument('start', 0),
            'length': self.get_argument('length', 10)
        }

        order_colume_str = 'columns[%s][data]' % self.get_argument('order[0][column]',0)
        order_colume = self.get_argument(order_colume_str,None)
        sort_dict = {
            'order_colume': order_colume,
            'order_type': self.get_argument('order[0][dir]', 'acs')
        }

        server = ServerModel()
        total_lines = yield server.get_server_total()
        data_list = yield server.get_server_list(limit_dict,sort_dict)

        return_json = dict()
        if data_list:
            for item in data_list:
                idc = IdcModel()
                idc.idc_id = item['idc_id']
                item['idc_id'] = yield idc.get_name_cn_by_id()

        return_json['draw'] = self.get_argument('draw')
        return_json['recordsTotal'] = total_lines
        return_json['recordsFiltered'] = total_lines

        return_json['data'] = data_list
        self.write(return_json)


    #新增服务器
    @coroutine
    @authenticated
    def post(self):
        server = ServerModel()
        server_json = json_decode(self.request.body)

        table_cols = yield server.dal.get_table_field()
        insert_keys = self.get_row_dict(server_json, table_cols)

        add_dict = dict()
        for key in insert_keys:
            add_dict[key] = server_json[key]

        try:
            result = yield server.add_server(add_dict)
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))

    #更新服务器
    @coroutine
    @authenticated
    def patch(self):
        server = ServerModel()
        server_json = json_decode(self.request.body)

        table_cols = yield server.dal.get_table_field()
        update_keys = self.get_row_dict(server_json, table_cols)

        update_dict = dict()
        for key in update_keys:
            update_dict[key] = server_json[key]

        search_dict = {
            server.dal.manager_ip: update_dict['manager_ip']
        }

        try:
            result = yield server.update_server(update_dict, search_dict)
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0,result))


    #删除服务器
    @coroutine
    @authenticated
    def delete(self):
        pass


#获取server的IP地址
@route('/api/async/v1/server/ip/(.*)')
class GetServerIpByNameHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self, server_name):
        server = ServerModel()
        server.server_name = server_name
        try:
            result = yield server.get_server_ip_by_name()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))


#获取server的信息地址
@route('/api/async/v1/server/info')
class GetServerByNameHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        server = ServerModel()
        try:
            arg = self.get_argument('condition', None)
            search_value = self.get_argument('value',None)
            result = -1
            if arg:
                if arg == 'server_name':
                    server.server_name = search_value
                    result = yield server.get_server_by_name()
                elif arg == 'manager_ip':
                    server.manager_ip = search_value
                    result = yield server.get_server_by_manager_ip()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))


@route('/api/async/v1/servers/list')
class GetServerListHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        server = ServerModel()
        result = yield server.get_server_name_list()
        if result == 0:
            self.write(self.return_json(1,'None'))
        elif result == -1:
            self.write(self.return_json(-1, 'Error'))
        else:
            server_list = result
            server_name_list = []
            for item in server_list:
                server_name_list.append(item['server_name'])
            self.write(self.return_json(0, server_name_list))

#获取各项服务器的状态
@route('/api/async/v1/servers/count')
class GetServerStatusList(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        server = ServerModel()
        try:
            result = yield server.get_servers_count()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))