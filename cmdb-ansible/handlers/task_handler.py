from __future__ import print_function
from tornado.gen import coroutine
from tornado.log import gen_log
from tornado.escape import json_decode
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from operator import eq
import sys
sys.path.append('.')
from wrapper.route import route
from handlers.base_handler import BaseHandler
from service.firewalld_service import FirewalldService
from service.hostname_service import HostNameService
from service.shell_service import ShellService
from service.user_service import UserService
from service.yum_repo_service import YumRepoService
from service.yum_service import YumService
from service.copy_service import CopyService
from service.systemd_service import SystemdService
@route('/ansible/task')
class TaskHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @run_on_executor
    @coroutine
    def post(self):
        ansible_json = json_decode(self.request.body)

        if 'module' not in ansible_json:
            self.write(self.return_json(1, 'No Module'))
            return

        module = ansible_json['module']

        if eq(module, 'yum'):
            yield self.yum(ansible_json)
        elif eq(module, 'yum_repo'):
            yield self.yum_repo(ansible_json)
        elif eq(module, 'shell'):
            yield self.shell(ansible_json)
        elif eq(module, 'user'):
            yield self.user(ansible_json)
        elif eq(module, 'firewalld'):
            yield self.firewalld(ansible_json)
        elif eq(module, 'hostname'):
            yield self.hostname(ansible_json)
        elif eq(module, 'copy'):
            yield self.copy(ansible_json)
        elif eq(module, 'systemd'):
            yield self.systemd(ansible_json)
        else:
            self.write(self.return_json(2, "Module Not Support"))

    @coroutine
    def yum(self, ansible_json):
        try:
            ys = YumService(ansible_json)
            result = yield ys.run_yum_service()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            gen_log.info(result)
            self.write(result)

    @coroutine
    def yum_repo(self, ansible_json):
        try:
            yrs = YumRepoService(ansible_json)
            yrs_result = yield yrs.run_repo()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            gen_log.info(yrs_result)
            self.write(yrs_result)

    @coroutine
    def shell(self, ansible_json):

        shell_service = ShellService(ansible_json)
        try:
            shell_result = yield shell_service.run_shell()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            gen_log.info(shell_result)
            self.write(shell_result)

    @coroutine
    def user(self, ansible_json):
        us = UserService(ansible_json)
        try:
            if eq(ansible_json['state'], 'absent'):
                result = yield us.del_user()
            elif eq(ansible_json['state'], 'present'):
                result = yield us.add_user()
            elif eq(ansible_json['state'], 'update'):
                result = yield us.update_password()
            else:
                result = self.return_json(2, 'Not Supported')
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

    @coroutine
    def firewalld(self, ansible_json):
        fs = FirewalldService(ansible_json)
        try:
            if 'service' in ansible_json:
                result = yield fs.run_service()
            elif 'port' in ansible_json:
                result = yield fs.run_port()
            elif 'source' in ansible_json:
                result = yield fs.run_source()
            elif 'masquerade' in ansible_json:
                result = yield fs.run_masquerade()
            else:
                result = self.return_json(2, 'Not Supported')
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

    @coroutine
    def hostname(self, ansible_json):
        host_name = HostNameService(ansible_json)
        try:
            result = yield host_name.run_hostname()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

    @coroutine
    def copy(self, ansible_json):
        cp = CopyService(ansible_json)
        try:
            result = yield cp.copy()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

    @coroutine
    def systemd(self, ansible_json):
        sm = SystemdService(ansible_json)

        try:
            result = yield sm.systemd()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

