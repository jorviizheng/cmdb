from __future__ import print_function
from tornado.gen import coroutine,Return
from operator import eq
import sys
sys.path.append('.')
from model.yum_repo_model import YumRepoModule
from service.base_service import BaseService


class YumRepoService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def run_repo(self):
        yum_repo = YumRepoModule(self.ansible_json)
        play_tasks_list = list()
        if eq(yum_repo.state, 'absent'):
            play_tasks_list.append(yum_repo.yum_remove_repo())
        elif eq(yum_repo.state, 'present'):
            play_tasks_list.append(yum_repo.yum_add_repo())

        try:
            result = yield self.run(play_tasks_list)
        except Exception as ex:
            raise ex
        else:
            raise Return(result)