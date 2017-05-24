import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from dal.tag_map_dal import TagMapDal


class TagMapModel(object):

    def __init__(self):
        self.dal = TagMapDal()
        self.tm_id = 1
        self.tid = 1
        self.server = []
        self.software = []

    def set_tag_map(self, tag_tuple=tuple()):
        self.tm_id = tag_tuple[0]
        self.tid = tag_tuple[1]
        self.server = tag_tuple[2]
        self.software = tag_tuple[3]

    def get_model_json(self):
        return {
            self.dal.tm_id: self.tm_id,
            self.dal.tid: self.tid,
            self.dal.server: self.server,
            self.dal.software: self.software
        }

    def get_model_list(self, result):
        if result == 0:
            return 0
        elif result == -1:
            return -1
        elif isinstance(result,tuple):
            tag_list = []
            return_tag = TagMapModel()
            if isinstance(result[0],tuple):
                for item in result:
                    return_tag.set_tag_map(item)
                    tag_list.append(return_tag.get_model_json())
            else:
                return_tag.set_tag_map(result)
                tag_list.append(return_tag.get_model_json())
            return tag_list

    @coroutine
    def add(self, add_dict):
        try:
            result = yield self.dal.insert(add_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    @coroutine
    def get_tag_map_by_id(self):
        search_dict = {
            self.dal.tid: self.tid
        }
        try:
            tag = yield self.dal.select('*', search_dict, None)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            if tag != 0:
                tag = tag[0]

            raise Return(tag)

    @coroutine
    def get_tag_map(self, search_dict=None, limit_dict=None):
        try:
            tags = yield self.dal.select('*', search_dict, limit_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(tags)

    @coroutine
    def update(self, update_dict):
        search_dict = {
            self.dal.tid: self.tid
        }
        try:
            result = yield self.dal.update(update_dict, search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    @coroutine
    def delete(self):
        search_dict = {
            self.dal.tid: self.tid
        }
        try:
            result = yield self.dal.delete(search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    @coroutine
    def get_servers_by_id(self):
        col_dict = {
            self.dal.server: self.dal.server
        }
        search_dict = {
            self.dal.tid: self.tid
        }
        try:
            result = yield self.dal.select(col_dict, search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            if result != 0:
                result = result[0][self.dal.server]
            raise Return(result)

    #更新server和tag_map
    @coroutine
    def update_server_map(self, new_servers):
        update_dict = {
            self.dal.server: new_servers
        }
        search_dict = {
            self.dal.tid: self.tid
        }
        try:
            result = yield self.dal.update(update_dict, search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)
