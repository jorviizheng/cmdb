import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from datetime import datetime
from dal import task_dal

DATETIME_FMT = '%Y-%m-%d %H:%M:%S' 


class TaskModel(object):

    def __init__(self):
        self.dal = task_dal.TaskDal()
        self.user_name = None
        self.task_status_id = 1
        self.task_name = ''
        self.task_type = ''
        self.task_flag = ''
        self.task_args = ''
        self.result = None
        self.create_time = None
        self.update_time = None


    def set_task(self,task_tuple=tuple()):
        self.task_id = task_tuple[0]
        self.user_name = task_tuple[1]
        self.task_status_id = task_tuple[2]
        self.task_name = task_tuple[3]
        self.task_type = task_tuple[4]
        self.task_flag = task_tuple[5]
        self.task_args = task_tuple[6]
        self.result = task_tuple[7]
        self.create_time = datetime.strftime(task_tuple[8],DATETIME_FMT)
        self.update_time = datetime.strftime(task_tuple[9],DATETIME_FMT)
            
    def get_model_json(self):
        return {
            self.dal.user_name:self.user_name,
            self.dal.task_status_id:self.task_status_id,
            self.dal.task_type:self.task_type,
            self.dal.task_flag:self.task_flag,
            self.dal.task_args:self.task_args,
            self.dal.create_time:self.create_time,
            self.dal.update_time:self.update_time,
            self.dal.task_name:self.task_name,
            self.dal.result:self.result
        }

    @coroutine
    def get_task_by_status(self, limit_dict=None):
        col_dict = '*'
        search_dict = {
            self.dal.task_status_id: self.task_status_id
        }
        result = yield self.dal.select(col_dict,search_dict,limit_dict)
        if result != 0:
            for item in result:
                item[self.dal.update_time] = datetime.strftime(item[self.dal.update_time], DATETIME_FMT)
                item[self.dal.create_time] = datetime.strftime(item[self.dal.create_time], DATETIME_FMT)

        raise Return(result)

    @coroutine
    def get_task_total(self):
        result = yield self.dal.select('*', None)
        if isinstance(result,int):
            raise Return(result)
        elif isinstance(result,tuple):
            raise Return(len(result))

    @coroutine
    def get_task(self, limit_dict=None, order_dict=None):
        col_dict = '*'
        result = yield self.dal.select(col_dict, None, limit_dict, order_dict)
        if result != 0:
            for item in result:
                item[self.dal.update_time] = datetime.strftime(item[self.dal.update_time], DATETIME_FMT)
                item[self.dal.create_time] = datetime.strftime(item[self.dal.create_time], DATETIME_FMT)

        raise Return(result)

    @coroutine
    def add_task(self):
        col_dict = {
            self.dal.task_name:self.dal.task_name
        }   
        search_dict = {
            self.dal.task_name: self.task_name, 
        }
        try:
            duplicate_name = yield self.dal.select(col_dict, search_dict)
        except Exception as err:
            raise err
        else:
            if duplicate_name != 0:
                raise Return(-1)
            else:
                try:
                    add_dict = self.get_model_json()
                except Exception as err:
                    print(err)
                    raise err
                result = yield self.dal.insert(add_dict)
                raise Return(result)

    @coroutine
    def update_task(self):
        update_dict = {
            self.dal.task_status_id:self.task_status_id,
            self.dal.result:self.result,
            self.dal.update_time:self.update_time
        }
        search_dict = {
            self.dal.task_name:self.task_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def delete(self):
        search_dict = {
            self.dal.task_name:self.task_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)  

    #获取任务总数和失败任务总数
    @coroutine
    def get_tasks_count(self):
        try:
            total_server_sql = 'select count(*)  from task'
            total_count = yield self.dal.execute(total_server_sql)

            error_server_sql = 'select count(*) from task where task_status_id = 5'
            error_count = yield self.dal.execute(error_server_sql)

            result = dict()
            result['total_count'] = total_count if total_count == 0 else total_count[0]['count']
            result['error_count'] = error_count if error_count == 0 else error_count[0]['count']
        except Exception as error:
            gen_log.error(error)
            raise error
        else:
            raise Return(result)