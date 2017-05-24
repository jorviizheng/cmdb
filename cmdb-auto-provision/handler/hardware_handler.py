# -*- coding: utf-8 -*-
from __future__ import print_function

from tornado.gen import coroutine

from handler.base_handler import BaseHandler
from utils.ilo4_util import Ilo4Util

import sys
sys.path.append('.')

from wrapper.route import route, authenticated


@route('/provision/v1/hardware/mac_addr/(.*)')
class GetILOMacAddr(BaseHandler):

    #获取Mac地址
    @coroutine
    @authenticated
    def get(self, manager_ip):
        ilo_client = Ilo4Util(manager_ip, 'admin', 'cGFzc3dvcmQ=')
        try:
            mac_list = yield ilo_client.get_mac_address()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, mac_list))



