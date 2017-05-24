from __future__ import print_function
from tornado.web import HTTPError
from tornado.gen import coroutine

import sys
sys.path.append('.')
from handlers.base_handler import BaseHandler
from service.hardware_service import HardwareService
from wrapper.route import route, authenticated


@route('/api/sync/v1/hardware/mac_addr/(.*)')
class GetMacAddressList(BaseHandler):
    @coroutine
    @authenticated
    def get(self, manager_ip):
        cookie = self.request.headers['Cookie']
        hardware = HardwareService(manager_ip, cookie)
        try:
            result = yield hardware.get_mac_list()
        except HTTPError as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(result)

