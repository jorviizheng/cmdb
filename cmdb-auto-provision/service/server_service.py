from __future__ import print_function

import sys

sys.path.append('.')

from tornado.gen import Return, coroutine
from tornado.httpclient import HTTPError
from tornado.locale import gen_log

from service.base_service import BaseService


class ServerService(BaseService):

    @coroutine
    def add_server(self):
        try:
            yield self.install_server()
        except HTTPError as err:
            raise err
        except Exception as err:
            raise err
        else:
            gen_log.info('Start Installing Server %s' % self.server_name)
            raise Return('Start Installing Server %s' % self.server_name)

    @coroutine
    def reship_server(self):
        try:
            yield self.install_server()
        except HTTPError as error:
            gen_log.error(error)
            raise error
        except Exception as err:
            raise err
        else:
            gen_log.info('Start Reinstalling Server %s' % self.server_name)
            raise Return('Start Reinstalling Server %s' % self.server_name)










