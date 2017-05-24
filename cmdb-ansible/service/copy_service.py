from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from model.copy_model import CopyModel
from service.base_service import BaseService


class CopyService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def copy(self):
        try:
            cp = CopyModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(cp.create_task())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)
