from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from model.systemd_model import SystemdModel
from service.base_service import BaseService


class SystemdService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)


    @coroutine
    def systemd(self):
        try:
            sm = SystemdModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(sm.systemd_task())
            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)
