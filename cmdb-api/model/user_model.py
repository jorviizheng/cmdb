import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import user_dal


class UserModel(object):

    def __init__(self):
        self.dal = user_dal.UserDal()
        self.user_name = ''
        self.user_password = ''
        self.name = None
        self.email = None
        self.mobile = None
        self.join_date = None
        self.last_login = None
        self.gid_list = None

    def get_model_json(self):
        return {
            self.dal.user_name:self.user_name,
            self.dal.user_password:self.user_password,
            self.dal.name:self.name,
            self.dal.email:self.email,
            self.dal.mobile:self.mobile,
            self.dal.join_date:self.join_date,
            self.dal.last_login:self.last_login,
            self.dal.gid_list:self.gid_list
        }

    @coroutine
    def add_user(self):
        col_dict = {
            self.dal.user_name:self.dal.user_name
        }   
        search_dict = {
            self.dal.user_name: self.user_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

    @coroutine
    def update_user_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.user_name:self.user_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_user_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.user_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_user_password(self,password):
        update_dict = {
            self.dal.user_password: password
        }
        search_dict = {
            self.dal.user_name:self.user_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_login_date(self):
        update_dict = {
            self.dal.last_login:self.last_login,
        }
        search_dict = {
            self.dal.user_name:self.user_name
        }      
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_password(self):
        col_dict = {
            self.dal.user_password:self.dal.user_password
        }
        search_dict = {
            self.dal.user_name:self.user_name
        }
        result = yield self.dal.select(col_dict, search_dict)
        if isinstance(result, list):
            raise Return(result[0][self.dal.user_password])
        elif isinstance(result, int):
            raise Return('')

    @coroutine
    def get_id_by_name(self):
        col_dict = {
            self.dal.uid:self.dal.uid
        }
        search_dict = {
            self.dal.user_name:self.user_name
        }
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_user_by_name(self):
        search_dict = {
            self.dal.user_name:self.user_name
        }
        result = yield self.dal.delete(search_dict)
        raise Return(result)   
