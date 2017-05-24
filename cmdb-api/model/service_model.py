import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import service_dal


class ServiceModel(object):

    def __init__(self):
        self.dal = service_dal.ServiceDal()
        self.service_id = 1
        self.service_type = ''
        self.service_name = ''
        self.service_version = ''

    def get_model_json(self):
        return {
            self.dal.service_type:self.service_type,
            self.dal.service_name:self.service_name,
            self.dal.service_version:self.service_version
        }

    @coroutine
    def add_service(self):
        col_dict = {
            self.dal.service_name:self.dal.service_name
        }   
        search_dict = {
            self.dal.service_name: self.service_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_service_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.service_name:self.service_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_service_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.service_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.service_id:self.dal.service_id
        }
        search_dict = {
            self.dal.service_name:self.service_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_service_by_name(self):
        search_dict = {
            self.dal.service_name:self.service_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)