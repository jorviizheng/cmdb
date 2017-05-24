from __future__ import print_function
from tornado.gen import coroutine, Return
import sys
sys.path.append('.')
from model.shell_model import ShellModel
from service.base_service import BaseService


class ShellService(BaseService):

    def __init__(self, ansible_json):
        BaseService.__init__(self, ansible_json)

    @coroutine
    def run_shell(self):
        shell_model = ShellModel(self.ansible_json)
        play_tasks_list = list()
        play_tasks_list.append(shell_model.create_task())
        try:
            result = yield self.run(play_tasks_list)
        except Exception as ex:
            raise ex
        else:
            raise Return(result)