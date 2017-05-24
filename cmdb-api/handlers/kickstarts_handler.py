# -*- coding: utf-8 -*-
from __future__ import print_function
from tornado.gen import coroutine, Return
from tornado.escape import json_decode

from operator import eq


import sys
sys.path.append('.')


from model.kickstarts_model import KickstartsModel
from handlers.base_handler import BaseHandler
from wrapper.route import route, authenticated


@route('/api/async/v1/kickstarts/(.*)')
class DhcpServerHandler(BaseHandler):

    @coroutine
    @authenticated
    def get(self, kickstarts_profile_id):
        km = KickstartsModel()
        km.kickstarts_profile_id = kickstarts_profile_id
        try:
            kickstart_profile_name = yield km.get_file_name()
        except Exception as err:
            self.write(self.return_json(-1, err.args))
        else:
            self.write(self.return_json(0, kickstart_profile_name))
