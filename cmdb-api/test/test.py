# -*- coding: utf-8 -*- 
from __future__ import print_function

from tornado.web import RequestHandler,HTTPError,authenticated
from tornado.gen import coroutine,Return
from tornado.escape import json_decode,json_encode

from datetime import datetime


import json

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler



class TestHandler(BaseHandler):
    
    @authenticated
    @coroutine
    def get(self):
        print(self.cookies['cookie_id'])
        print(self.get_secure_cookie('cookie_id'))
        if self.cookies['cookie_id'] == self.get_secure_cookie('cookie_id'):
            print('eq')
        else:
            print('1111')
        result = yield self.echo()
        self.write(result)

    @coroutine
    def echo(self):
        raise Return('coroutine')


class ServerHandler(BaseHandler):   

    @authenticated
    @coroutine
    def post(self, *args, **kwargs):
        if len(args) == 0:
            self.write('1')
        elif args[0] == 'insert':
            result = yield self.add_idc()
            print('insert %s'% type(result))
            self.write('0')

    @coroutine
    def add_idc(self):
        body = self.request.body
        #json_dict = {'idc_name':'chongqing33355222','idc_name_cn':"重庆accccaaabbbb",'idc_address':"重庆dddb"}#json.loads(body.decode())
        # json_dict ={
        # 'server_name':'slave245',
        # 'manager_ip' : '172.16.250.24',
        # 'server_ip' : '172.16.251.24',
        # 'server_group' : 'test',
        # 'server_type' : '1111',
        # 'system_type': 'linux',
        # 'tag' : 'test',
        # 'status' : 'status',
        # 'machine_type' : 'machine_type' ,   
        # 'sn' : 'sn11',
        # 'cpu' : 'cpu11',
        # 'memory' : 'memory11',
        # 'hardisk': 'hardisk1',
        # 'raid':'raid',
        # 'rack_type':'rack_type'
        # }
        # json_dict={
        #     'group_name':'test',
        #     'uid_list':'1,2,3,4',
        #     'pid':'1'
        # }
        # arg_list = []
        # for key in json_dict:
        #     arg_list()
        
        #idc_md = idc_model.IdcModel(json_dict)
        #result =  yield idc_md.add_idc()#get_id_by_name() #yield self.db.get_idc_id_by_name("beijing")
        #result =  yield idc_md.update_idc_by_name()
        #result = yield idc_md.add_idc()
        #result = yield idc_md.delete_idc_by_name()

        # server_md = server_model.ServerModel(json_dict)
        # #result = yield server_md.add_server()
        # result = yield server_md.update_server_name('slave24')
        #result = yield server_md.delete_server_by_name()

        # group_md = group_model.GroupModel(json_dict)
        # #result = yield group_md.add_group()
        # #result = yield group_md.update_group_by_name()
        # # result = yield group_md.update_group_name("admin")
        # result = yield group_md.delete_group_by_name()
        
        # json_dict = {
        # 'user_name' : 'zengqi',
        # 'user_password' : '123123444555',
        # 'name':'曾',
        # 'email':'zengqi0529@163.com111',
        # 'mobile':'1832830836822',
        # 'join_date':datetime.now(),
        # 'last_login': datetime.now(),
        # 'gid_list':'0'
        # }
        # user_md = user_model.UserModel(json_dict)
        # #result = yield user_md.add_user()
        # #result = yield user_md.update_user_by_name()
        # #result = yield user_md.update_user_password_by_name('123')
        # result = yield user_md.update_login_date()

        # json_dict ={
        # 'p_name' : 'add',
        # 'p_name_cn': '新增',
        # 'rid' : 1,
        # 'value' : '123'
        # }
        # p_md = permisson_model.PermissonModel(json_dict)
        # #result = yield p_md.add_permisson()
        # #result = yield p_md.update_permisson_by_name()
        # #result = yield p_md.update_p_name('新增')
        # result = yield p_md.delete_permisson_by_name()

        # json_dict ={
        # 'resource_type' : 'url',
        # 'resource_name' : '/user/add/ccc',
        # 'resource_name_cn' : '新增用户'
        # }
        # r_md = resource_model.ResourceModel(json_dict)
        # #result = yield r_md.add_resource()
        # #result = yield r_md.update_resource_by_name()
        # # result = yield r_md.update_resource_name('/user/add')
        # result = yield r_md.delete_resource_by_name()
    #     json_dict = {
    #     'service_type' : 'ansible',
    #     'service_name' : 'set_host_name_new',
    #     'service_version' : '2.0'
    #     }
    #     service_dm = service_model.ServiceModel(json_dict)
    #    #result = yield service_dm.add_service()
    #     result = yield service_dm.update_service_by_name()
    #     result = yield service_dm.update_service_name('set_host_name')
    #     #result = yield service_dm.delete_service_by_name()

        # json_dict = {
        # 'service_id' : 2,
        # 'server_id':3,
        # 'create_date':datetime.now(),
        # 'last_excute_time':datetime.now()
        # }
        # ss_md = service_status_model.ServiceStatusModel(json_dict)
        # #result = yield ss_md.add_service_status()
        # #result = yield ss_md.update_last_excute_time()
        # result = yield ss_md.delete()

        # json_dict = {
        #     'task_status_name':'新建'
        # }
        # ts_md = task_status_model.TaskStatusModel(json_dict)
        # result = yield ts_md.add_task_status()
        # #result  = yield ts_md.update_task_status_name('新建')
        # #result = yield ts_md.delete()


        json_dict = {
        'user_name' : 'zengqi',
        'task_status_id' : 4,
        'task_type':'flow',
        'task_args':'bbb',
        'create_time':datetime.now(),
        'update_time':datetime.now(),
        'result':'result',
        }
        task_md = task_model.TaskModel(json_dict)
        #result = yield task_md.add_task()
        # print(task_md.task_status_id)
        # task_md.task_status_id = 6
        # result = yield task_md.update_task_status()
        task_md.task_name = 'zengqi_20170113202851'
        result= yield task_md.update_update_time()
        
        if result == 0 :
            print('none')
        else:
            print('insert %s' % result)
        
        raise Return(result)           