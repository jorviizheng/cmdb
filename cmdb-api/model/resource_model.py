import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import resource_dal


class ResourceModel(object):

    def __init__(self):
        self.dal = resource_dal.ResourceDal()
        self.rid = 1
        self.resource_type = ''
        self.resource_name = ''
        self.resource_name_cn = ''

    def get_model_json(self):
        return {
            self.dal.resource_type:self.resource_type,
            self.dal.resource_name:self.resource_name,
            self.dal.resource_name_cn:self.resource_name_cn
        }

    @coroutine
    def add_resource(self):
        col_dict = {
            self.dal.resource_name:self.dal.resource_name
        }   
        search_dict = {
            self.dal.resource_name: self.resource_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_resource_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.resource_name:self.resource_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_resource_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.resource_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)

        
    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.rid:self.dal.rid
        }
        search_dict = {
            self.dal.resource_name:self.resource_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_resource_by_name(self):
        search_dict = {
            self.dal.resource_name:self.resource_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)
