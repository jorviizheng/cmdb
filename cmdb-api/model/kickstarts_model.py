import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from dal.kickstarts_dal import KickstartsDal


class KickstartsModel(object):

    def __init__(self):
        self.dal = KickstartsDal()
        self.ksp_id = 1
        self.kickstarts_profile_path = ''
        self.kickstarts_profile_name = ''

    def get_model_json(self):
        model_json = {
            self.dal.ksp_id: self.ksp_id,
            self.dal.kickstarts_profile_path: self.kickstarts_profile_path,
            self.dal.kickstarts_profile_name: self.kickstarts_profile_name,
        }
        return model_json

    @coroutine
    def get_file_name(self):
        col_dict = {
            self.dal.kickstarts_profile_name: self.dal.kickstarts_profile_name
        }
        search_dict = {
            self.dal.ksp_id: self.ksp_id
        }
        result = yield self.dal.select(col_dict, search_dict)
        raise Return(result[0][self.dal.kickstarts_profile_name])