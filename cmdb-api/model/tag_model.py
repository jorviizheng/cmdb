import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from dal.tag_dal import TagDal


class TagModel(object):

    def __init__(self):
        self.dal = TagDal()
        self.tid = 1
        self.t_name = ''

    def set_tag(self, tag_tuple=tuple()):
        self.tid = tag_tuple[0]
        self.t_name = tag_tuple[1]

    def get_model_json(self):
        return {
            self.dal.tid: self.tid,
            self.dal.t_name: self.t_name
        }

    def get_model_list(self, result):
        if result == 0:
            return 0
        elif result == -1:
            return -1
        elif isinstance(result,tuple):
            tag_list = []
            return_tag = TagModel()
            if isinstance(result[0],tuple):
                for item in result:
                    return_tag.set_tag(item)
                    tag_list.append(return_tag.get_model_json())
            else:
                return_tag.set_tag(result)
                tag_list.append(return_tag.get_model_json())
            return tag_list

    @coroutine
    def add_tag(self):
        col_dict = {
            self.dal.t_name: self.t_name
        }
        search_dict = {
            self.dal.t_name: self.t_name
        }
        try:
            duplicate_name = yield self.dal.select(col_dict, search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            if duplicate_name == 0:
                add_dict = {
                    self.dal.t_name: self.t_name
                }
                result = yield self.dal.insert(add_dict)
                raise Return(result)

    @coroutine
    def get_tid_by_name(self):
        search_dict = {
            self.dal.t_name: self.t_name
        }
        try:
            t_id = yield self.dal.select('*', search_dict)
        except Exception as err:
            raise err
        else:
            if t_id != 0:
                t_id = t_id[0][self.dal.tid]
            raise Return(t_id)

    @coroutine
    def get_tag(self, search_dict=None, limit_dict=None):
        try:
            tags = yield self.dal.select('*', search_dict, limit_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            if tags != 0:
                for tag in tags:
                    tag = tag[self.dal.t_name]

            raise Return(tags)

    @coroutine
    def get_tag_count(self, search_dict=None, limit_dict=None):
        try:
            tags = yield self.dal.select('*', search_dict, limit_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            if tags != 0:
                tags = len(tags)
            raise Return(tags)

    @coroutine
    def update(self, new_name):
        update_dict = {
            self.dal.t_name: new_name
        }
        search_dict = {
            self.dal.t_name: self.t_name
        }
        try:
            result = yield self.dal.update(update_dict,search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)

    @coroutine
    def delete(self):
        search_dict = {
            self.dal.t_name: self.t_name
        }
        try:
            result = yield self.dal.delete(search_dict)
        except Exception as err:
            gen_log.error(err)
            raise err
        else:
            raise Return(result)
