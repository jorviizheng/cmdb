import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import task_status_dal


class TaskStatusModel(object):

    def __init__(self):
        self.dal = task_status_dal.TaskStatusDal()
        self.task_status_id = 1
        self.task_status_name = ''

    def get_model_json(self):
        return {
            self.dal.task_status_name:self.task_status_name
        }

    @coroutine
    def add_task_status(self):
        col_dict = {
            self.dal.task_status_name:self.dal.task_status_name
        }   
        search_dict = {
            self.dal.task_status_name: self.task_status_name,
            
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

    @coroutine
    def update_task_status_name(self, old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.task_status_name: old_name
        }
        result = yield self.dal.update(update_dict, search_dict)
        raise Return(result)

    
    @coroutine
    def get_task_id_by_name(self):
        search_dict = {
            self.dal.task_status_name:self.task_status_name
        }
        result = yield self.dal.select(search_dict)
        raise Return(result)

    @coroutine
    def get_task_name_by_id(self):
        col_dict = {
            self.dal.task_status_name,self.dal.task_status_name
        }
        search_dict = {
            self.dal.task_status_id:self.task_status_id
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result[0][self.dal.task_status_name])

    @coroutine
    def delete(self):
        search_dict = {
            self.dal.task_status_name:self.task_status_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)  
