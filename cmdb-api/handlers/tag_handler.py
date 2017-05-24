# -*- coding: utf-8 -*-from __future__ import print_functionfrom tornado.gen import coroutine, Returnfrom tornado.escape import json_decodefrom tornado.log import gen_logfrom operator import eq, neimport syssys.path.append('.')from model.tag_model import TagModelfrom model.tag_map_model import TagMapModelfrom model.server_model import ServerModelfrom handlers.base_handler import BaseHandlerfrom wrapper.route import route,authenticated@route('/api/async/v1/tags')class Tags(BaseHandler):    #获取Tag列表    @coroutine    def get(self):        limit_dict = {            'start': self.get_argument('start', 0),            'length': self.get_argument('length', 10)        }        tag = TagModel()        total_lines = yield tag.get_tag_count()        data_list = yield tag.get_tag(None, limit_dict)        return_json = dict()        return_json['draw'] = self.get_argument('draw')        return_json['recordsTotal'] = total_lines        return_json['recordsFiltered'] = total_lines        return_json['data'] = data_list        self.write(return_json)    #新增tag    @coroutine    def post(self):        tag_json = json_decode(self.request.body)        tm = TagModel()        tm.t_name = tag_json['t_name']        try:            add_tag = yield tm.add_tag()        except Exception as err:            self.write(self.return_json(-1, err.args))        else:            self.write(self.return_json(0, add_tag))    #更新    @coroutine    def patch(self):        tag_json = json_decode(self.request.body)        tm = TagModel()        tm.t_name = tag_json['t_name']        new_name = tag_json['new_name']        try:            update_tag = yield tm.update(new_name)        except Exception as err:            self.write(self.return_json(-1, err.args))        else:            self.write(self.return_json(0, update_tag))    #删除tag    #参数:t_name tag名称    @coroutine    def delete(self):        try:            t_name = self.get_argument('t_name')        except Exception as err:            self.write(self.return_json(-1, 'No Args: t_name'))        else:            tm = TagModel()            tm.t_name = t_name            try:                tag_id = yield tm.get_tid_by_name()                if eq(tag_id, 0):                    self.write(self.return_json(1, 0))                    return                else:                    search_dict = dict()                    search_dict['tid'] = tag_id                    tmm = TagMapModel()                    used_tag = yield tmm.get_tag_map(search_dict)                    #没有被使用                    if eq(used_tag, 0):                        gen_log.info('Delete %s' % tm.t_name)                        delete_tag = yield tm.delete()                        self.write(self.return_json(0, delete_tag))                    else:                        server_map = used_tag[0]['server']                        software_map = used_tag[0]['software']                        server_flag = False                        software_flag = False                        if server_map is None or len(server_map) == 0:                            server_flag = True                        if software_map is None or len(software_map) == 0:                            software_flag = True                        if server_flag and software_flag:                            gen_log.info('Delete %s' % tm.t_name)                            delete_tag = yield tm.delete()                            self.write(self.return_json(0, delete_tag))                        else:                            gen_log.info('Tag used')                            self.write(self.return_json(1, 'Tag Used'))            except Exception as err:                self.write(self.return_json(-1, err.args))## 获取tag列表#@route('/api/async/v1/tag/list')class GetTagList(BaseHandler):    @coroutine    def get(self):        tag = TagModel()        data_list = yield tag.get_tag()        self.write(self.return_json(0, data_list))@route('/api/async/v1/tag/(.*)/(.*)')class TagAction(BaseHandler):    #    # 通过tag查询资源    # 接收2个参数    # 1 tag类型    # 2 tag名称    @coroutine    def get(self, t_type, t_name):        search_dict = dict()        search_dict['t_name'] = t_name        tmm = TagMapModel()        tm = TagModel()        try:            tm.t_name = t_name            tid = yield tm.get_tid_by_name()            #不存在该tag            if eq(tid, 0):                self.write(self.return_json(0, 0))                return            else:                tmm.tid = tid                tag = yield tmm.get_tag_map_by_id()        except Exception as err:            raise err        else:            #不存在map映射关系            if eq(tid, 0):                self.write(self.return_json(0, tag))            else:                result_list = list()                if eq(t_type, 'server'):                    search_str = tag['server']                    server = ServerModel()                    result_list = yield server.get_server_for_tag(search_str)                elif eq(t_type, 'software'):                    search_str = tag['software']                    result_list = [1, 2, 3]                self.write(self.return_json(0, result_list))    #    # 资源上tag    # 接收2个参数    # 1 tag类型    # 2 tag名称    @coroutine    def post(self, t_type, t_name):        tag_json = json_decode(self.request.body)        resource_name = tag_json['name']        try:            #检查tag是否存在            yield self.__add_tag(t_name)            if eq(t_type, 'server'):                yield self.add_server_tag(t_name, resource_name)        except Exception as err:            self.write(self.return_json(-1, err.args))    # 资源删tag    # 接收2个参数    # 1 tag类型    # 2 tag名称    @coroutine    def patch(self, t_type, t_name):        tag_json = json_decode(self.request.body)        resource_name = tag_json['name']        if eq(t_type, 'server'):            yield self.delete_server_tag(t_name, resource_name)    #增加新tag    @coroutine    def __add_tag(self, t_name):        tm = TagModel()        tm.t_name = t_name        try:            tid = yield tm.get_tid_by_name()            if tid == 0:                yield tm.add_tag()        except Exception as err:            raise err    #取消server tag    @coroutine    def delete_server_tag(self, t_name, resource_name):        try:            # 检查tag_map的映射是否存在            tmm = TagMapModel()            tm = TagModel()            tm.t_name = t_name            tmm.tid = yield tm.get_tid_by_name()            tag_map = yield tmm.get_tag_map_by_id()            # 检查资源是否有这个tag            sm = ServerModel()            sm.server_name = resource_name            sm.server_id = yield sm.get_id_by_name()            old_tags = yield sm.get_tag_by_id()            #server存在该标签            del_tag_map_result = 0            del_server_result = 0            if t_name in old_tags:                if tag_map:                    old_server_map = tag_map[tmm.dal.server]                    # 检查该tag_map是否有该映射                    if str(sm.server_id) in old_server_map:                        del_tag_map_result = yield self.__del_tag_server_map(t_name, resource_name)                del_server_result = yield self.__del_server_tag(t_name, resource_name)        except Exception as err:            self.write(self.return_json(-1, err.args))        else:            self.write(self.return_json(0, del_tag_map_result+del_server_result))    #添加server tag    @coroutine    def add_server_tag(self, t_name, resource_name):        tmm = TagMapModel()        tm = TagModel()        sm = ServerModel()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        tm.t_name = t_name        tmm.tid = yield tm.get_tid_by_name()        add_tag_result = 0        add_tag_map_result = 0        #检查server是否有这个tag        old_tags = yield sm.get_tag_by_id()        if t_name not in old_tags:            tag_map = yield tmm.get_tag_map_by_id()            if not tag_map:                add_tag_map_result = yield self.__add_tag_server_map(t_name, resource_name)            else:                add_tag_map_result = yield self.__update_tag_server_map(t_name, resource_name)            add_tag_result = yield self.__add_server_tag(t_name, resource_name)        self.write(self.return_json(0, add_tag_result+add_tag_map_result))    #增加tag_map中对应server的映射    @coroutine    def __add_tag_server_map(self, t_name, resource_name):        tmm = TagMapModel()        tm = TagModel()        sm = ServerModel()        tm.t_name = t_name        tmm.tid = yield tm.get_tid_by_name()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        map_add_dict = {            tmm.dal.tid: tmm.tid,            tmm.dal.server: sm.server_id        }        add_tag_server = yield tmm.add(map_add_dict)        raise Return(add_tag_server)    #更新tag_map中对应的server映射    @coroutine    def __update_tag_server_map(self, t_name, resource_name):        sm = ServerModel()        tmm = TagMapModel()        tm = TagModel()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        # 设置新的tag_map 映射        tm.t_name = t_name        tmm.tid = yield tm.get_tid_by_name()        tag_map = yield tmm.get_tag_map_by_id()        old_servers = tag_map['server']        new_servers = ''        if old_servers:            if str(sm.server_id) in old_servers:                new_servers = old_servers            elif len(old_servers) == 0:                new_servers = sm.server_id            else:                new_servers = old_servers + ',' + str(sm.server_id)        else:            new_servers = sm.server_id        add_tag_map = yield tmm.update_server_map(new_servers)        raise Return(add_tag_map)    #删除tag_map中对应server的映射值    @coroutine    def __del_tag_server_map(self, t_name, resource_name):        sm = ServerModel()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        # 设置新的tag_map 映射        tmm = TagMapModel()        tm = TagModel()        tm.t_name = t_name        tmm.tid = yield tm.get_tid_by_name()        new_server_map_list = list()        tag_map = yield tmm.get_tag_map_by_id()        if tag_map == 0:            self.write(self.return_json(1, 'No Tags Map'))            return        old_server_map = tag_map['server']        for sid in old_server_map.split(','):            if ne(str(sm.server_id), sid):                new_server_map_list.append(sid)        new_servers = ','.join(new_server_map_list)        del_tag_map = yield tmm.update_server_map(new_servers)        yield self.__del_tag_map_line(tmm.tid)        raise Return(del_tag_map)    #删除tag_map整条记录    # 如果不存在任何映射，便删除该行    @coroutine    def __del_tag_map_line(self, tid):        try:            tmm = TagMapModel()            tmm.tid = tid            tag_map = yield tmm.get_tag_map_by_id()            key_list =list()            for key in tag_map.keys():                if ne(key, tmm.dal.tid) and ne(key, tmm.dal.tm_id):                    key_list.append(key)            null_col_number =0            for key in key_list:                if tag_map[key] == '' or tag_map[key] is None:                    null_col_number += 1            if len(key_list) == null_col_number:                yield tmm.delete()        except Exception as err:            raise err    #增加server表中的tag标签    @coroutine    def __add_server_tag(self, t_name, resource_name):        sm = ServerModel()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        old_tags = yield sm.get_tag_by_id()        new_tags = ''        if old_tags:            if t_name in old_tags:                new_tags = old_tags            elif len(old_tags) == 0:                new_tags = t_name            else:                new_tags = old_tags + ',' + t_name        else:            new_tags = t_name        add_tag = yield sm.update_tag(new_tags)        raise Return(add_tag)    #删除server表中的tag标签    @coroutine    def __del_server_tag(self, t_name, resource_name):        # 设置server 新tag标签        sm = ServerModel()        sm.server_name = resource_name        sm.server_id = yield sm.get_id_by_name()        old_tags = yield sm.get_tag_by_id()        if not old_tags:            self.write(self.return_json(1, 'No Tags'))            return        new_tag_list = list()        for tag in old_tags.split(','):            if ne(tag, t_name):                new_tag_list.append(tag)        new_tags = ','.join(new_tag_list)        del_server = yield sm.update_tag(new_tags)        raise Return(del_server)