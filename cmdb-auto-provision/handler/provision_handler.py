# -*- coding: utf-8 -*-
from __future__ import print_function

from tornado.gen import coroutine
from tornado.escape import json_decode
from tornado.httpclient import HTTPError
from tornado.concurrent import run_on_executor


from handler.base_handler import BaseHandler
from service.server_service import ServerService
from utils.ssh_util import Ssh

import sys
sys.path.append('.')

from wrapper.route import route, authenticated


@route('/provision/v1/server')
class ProvisionHandler(BaseHandler):

    #新安装服务器
    # @run_on_executor
    @coroutine
    @authenticated
    def post(self):

        provision_json = json_decode(self.request.body)
        async_api_url = yield self.get_async_api_service()
        cookie = yield self.get_async_api_cookie()
        ansible_url = yield self.get_ansible_service()
        ad = ServerService(cookie,async_api_url,ansible_url,provision_json)

        try:
            result = yield ad.add_server()
        except HTTPError as err:
            self.write(self.return_json(-1, err.message))
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))

    #重装服务器
    # @run_on_executor
    @coroutine
    @authenticated
    def put(self):
        provision_json = json_decode(self.request.body)
        async_api_url = yield self.get_async_api_service()
        cookie = yield self.get_async_api_cookie()
        ansible_url = yield self.get_ansible_service()
        ad = ServerService(cookie,async_api_url,ansible_url,provision_json)
        try:
            result = yield ad.reship_server()
        except HTTPError as err:
            self.write(self.return_json(-1, err.message))
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, result))


#查询装机是否成功
@route('/provision/v1/server/check')
class CheckServerInstallResult(BaseHandler):
    @run_on_executor
    @coroutine
    def get(self):
        try:
            server_ip = self.get_argument('server_ip')
            ssh = Ssh(server_ip)
            result = yield ssh.ssh_connect()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(result, '%s Install Success' % server_ip))
