from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from model.hostname_model import HostnameModel
from service.base_service import BaseService


class HostNameService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def run_hostname(self):
        try:
            host_name = HostnameModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(host_name.create_task())
            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

