import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal import idc_dal


class IdcModel(object):

    def __init__(self):
        self.dal = idc_dal.IdcDal()
        self.idc_id = 1
        self.idc_name = ''
        self.idc_name_cn = ''
        self.idc_address = ''

        self.idc_json = dict()

    def get_model_json(self):
        idc_json = {
            self.dal.idc_name:self.idc_name,
            self.dal.idc_name_cn:self.idc_name_cn,
            self.dal.idc_address:self.idc_address
        }
        return idc_json

    def __get_idc_name_json(self):
        return {
            self.dal.idc_name:self.idc_name
        }

    def __get_idc_id_json(self):
        return {
            self.dal.idc_id:self.dal.idc_id
        }

    @coroutine
    def add_idc(self):
        col_dict = {
            self.dal.idc_name:self.dal.idc_name
        }   
        search_dict = {
            self.dal.idc_name: self.idc_name
        }
        duplicate_name = yield self.dal.select(col_dict, search_dict)
        if duplicate_name != 0:
            raise Return(-1)
        else:
            add_dict = self.get_model_json()
            result = yield self.dal.insert(add_dict)
            raise Return(result)

        
    @coroutine
    def update_idc_by_name(self):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.idc_name:self.idc_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def update_idc_name(self,old_name):
        update_dict = self.get_model_json()
        search_dict = {
            self.dal.idc_name: old_name
        }
        result = yield self.dal.update(update_dict,search_dict)
        raise Return(result)

    @coroutine
    def get_id_by_name(self):
        search_dict = self.__get_idc_name_json()
        col_dict = self.__get_idc_id_json()
        result = yield self.dal.select(col_dict,search_dict)
        raise Return(result)
    
    @coroutine
    def delete_idc_by_name(self):
        search_dict = self.__get_idc_name_json()
        result = yield self.dal.detele(search_dict)
        raise Return(result)

    @coroutine
    def get_idc_field(self):
        raise Return(self.dal.return_field())

    @coroutine
    def get_id_by_name_cn(self):
        col_dict = self.__get_idc_id_json()
        search_dict = {
            self.dal.idc_name_cn:self.idc_name_cn
        }
        result = yield self.dal.select(col_dict, search_dict)
        if result != 0:
            result = result[0][self.dal.idc_id]
        raise Return(result)

    @coroutine
    def get_name_cn_by_id(self):
        col_dict = {
            self.dal.idc_name_cn:self.dal.idc_name_cn
        }
        search_dict ={
            self.dal.idc_id:self.idc_id
        }
        result = yield self.dal.select(col_dict,search_dict)
        if result != 0:
            result = result[0][self.dal.idc_name_cn]
        raise Return(result)