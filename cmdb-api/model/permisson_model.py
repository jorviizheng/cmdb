import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import permisson_dal


class PermissonModel(object):

    def __init__(self):
        self.dal = permisson_dal.PermissonDal()
        self.pid = 1
        self.p_name = ''
        self.p_name_cn = ''
        self.rid = 1
        self.value = ''


    def get_model_json(self):
        return {
            self.dal.p_name:self.p_name,
            self.dal.p_name_cn:self.p_name_cn,
            self.dal.rid:self.rid,
            self.dal.value:self.value
        }

    @coroutine
    def add_permisson(self):
        col_dict = {
            self.dal.p_name:self.dal.p_name
        }   
        search_dict = {
            self.dal.p_name: self.p_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_permisson_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.p_name:self.p_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_p_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.p_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.pid:self.dal.pid
        }
        search_dict = {
            self.dal.p_name:self.p_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_permisson_by_name(self):
        search_dict = {
            self.dal.p_name:self.p_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)