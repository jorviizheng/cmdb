from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from model.user_model import UserModel
from service.base_service import BaseService


class UserService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def add_user(self):
        try:
            um = UserModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(um.add_user())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

    @coroutine
    def del_user(self):
        try:
            um = UserModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(um.del_user())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

    @coroutine
    def update_password(self):
        try:
            um = UserModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(um.change_password())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)