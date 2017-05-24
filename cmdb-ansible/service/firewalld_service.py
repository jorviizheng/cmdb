from __future__ import print_function

import sys
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from model.firewalld_model import FirewalldModel
from service.base_service import BaseService


class FirewalldService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def run_service(self):
        try:
            fm = FirewalldModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(fm.firewall_service())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

    @coroutine
    def run_port(self):
        try:
            fm = FirewalldModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(fm.firewall_port())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

    @coroutine
    def run_source(self):
        try:
            fm = FirewalldModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(fm.firewall_source())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)

    @coroutine
    def run_masquerade(self):
        try:
            fm = FirewalldModel(self.ansible_json)
        except Exception as error:
            gen_log.error(error.args)
            raise Exception('Args Wrong:%s' % error.args)
        else:
            play_tasks_list = list()
            play_tasks_list.append(fm.firewall_masquerade())

            try:
                result = yield self.run(play_tasks_list)
            except Exception as ex:
                raise ex
            else:
                raise Return(result)