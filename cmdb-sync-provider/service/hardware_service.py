from __future__ import print_function

from tornado.gen import coroutine, Return
from tornado.escape import json_decode
from tornado.log import gen_log
from tornado.web import HTTPError
import sys

sys.path.append('.')
from service.base_service import BaseService
from utils.http_util import http_client


class HardwareService(BaseService):

    def __init__(self, manager_ip, cookie):
        self.manager_ip = manager_ip
        BaseService.__init__(self, None, cookie)

    @coroutine
    def get_mac_list(self):
        try:
            provision_service = yield self.get_provision_service()
            provision_url = 'http://%s/provision/v1/hardware/mac_addr/%s' % (provision_service, self.manager_ip)
            response = yield http_client(provision_url, 'GET', self.cookie, None, 120)
        except HTTPError as err:
            gen_log.info(err)
            raise err
        else:
            result = response.body
            raise Return(result)


