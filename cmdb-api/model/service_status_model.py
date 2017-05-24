import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from datetime import datetime

from dal import service_status_dal


class ServiceStatusModel(object):

    def __init__(self):
        self.dal = service_status_dal.ServiceStatusDal()
        self.service_status_id = 1
        self.service_id = ''
        self.server_id = ''
        self.create_date = datetime.now()
        self.last_excute_time = datetime.now()

    def get_model_json(self):
        return {
            self.dal.service_id:self.service_id,
            self.dal.server_id:self.server_id,
            self.dal.create_date:self.create_date,
            self.dal.last_excute_time:self.last_excute_time
        }

    @coroutine
    def add_service_status(self):
        col_dict = {
            self.dal.service_id:self.dal.service_id,
            self.dal.server_id:self.dal.server_id
        }   
        search_dict = {
            self.dal.service_id: self.service_id,
            self.dal.server_id: self.server_id
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_last_excute_time(self):
        update_dict = {
            self.dal.last_excute_time:self.last_excute_time
        }
        search_dict = {
            self.dal.service_id:self.service_id,
            self.dal.server_id: self.server_id
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def delete(self):
        search_dict = {
            self.dal.service_id:self.service_id,
            self.dal.server_id:self.server_id
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)
