from __future__ import print_function
from tornado.gen import coroutine, Return
from operator import eq

import copy

import sys
sys.path.append('.')
from service.base_service import BaseService
from model.yum_model import YumModule


class YumService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    def present(self):
        yum_module = YumModule(self.ansible_json)
        play_tasks_list = list()
        play_tasks_list.append(yum_module.yum_task())
        return play_tasks_list

    def absent(self):
        yum_module = YumModule(self.ansible_json)
        play_tasks_list = list()
        play_tasks_list.append(yum_module.yum_task())
        return play_tasks_list

    def update(self):
        absent_json = copy.deepcopy(self.ansible_json)
        present_json = copy.deepcopy(self.ansible_json)

        absent_json['package_name'] = absent_json['package_name'].split('-')[0]
        absent_json['state'] = 'absent'

        present_json['state'] = 'present'

        absent_module = YumModule(absent_json)
        present_module = YumModule(present_json)

        play_tasks_list = list()
        play_tasks_list.append(absent_module.yum_task())
        play_tasks_list.append(present_module.yum_task())

        return play_tasks_list

    @coroutine
    def run_yum_service(self):
        play_tasks_list = list()

        if eq(self.ansible_json['state'], 'present'):
            play_tasks_list = self.present()
        elif eq(self.ansible_json['state'], 'absent'):
            play_tasks_list = self.absent()
        elif eq(self.ansible_json['state'], 'last'):
            play_tasks_list = self.update()

        try:
            result = yield self.run(play_tasks_list)
        except Exception as ex:
            raise ex
        else:
            raise Return(result)
