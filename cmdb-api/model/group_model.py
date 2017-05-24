import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import group_dal


class GroupModel(object):
    def __init__(self):
        self.dal = group_dal.GroupDal()
        self.gid = 1
        self.group_name = ''
        self.uid_list = []
        self.pid = 1

    def get_model_json(self):
        return {
            self.dal.group_name:self.group_name,
            self.dal.uid_list:self.uid_list,
            self.dal.pid:self.pid
        }

    @coroutine
    def add_group(self):
        col_dict = {
            self.dal.group_name:self.dal.group_name
        }   
        search_dict = {
            self.dal.group_name: self.group_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_group_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.group_name:self.group_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_group_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.group_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.gid:self.dal.gid
        }
        search_dict = {
            self.dal.group_name:self.group_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_group_by_name(self):
        search_dict = {
            self.dal.group_name:self.group_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)   

        
    
    
