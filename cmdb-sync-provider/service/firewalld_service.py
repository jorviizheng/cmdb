from __future__ import print_function

from tornado.gen import coroutine, Return
from tornado.escape import json_decode
from tornado.log import gen_log
from tornado.web import HTTPError
import sys

sys.path.append('.')
from service.base_service import BaseService
from utils.http_util import http_client


class FirewalldServer(BaseService):

    def __init__(self, ansible_json, cookie):
        BaseService.__init__(self, ansible_json, cookie)
        self.get_zones_cmd = 'firewall-cmd --get-zones'
        self.get_service_cmd = 'firewall-cmd --get-services'

    @coroutine
    def get_zones(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.get_zones_cmd
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as err:
            gen_log.info(err)
            raise err
        else:
            result = json_decode(response.body)
            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                        zones = list()
                        for zone in host['msg'][0].split():
                            zones.append(zone)
                        host['msg'] = zones
            raise Return(result)


    @coroutine
    def get_services(self):
        try:
            ansible_service = yield self.get_ansible_service()
            ansible_url = 'http://%s/ansible/task' % ansible_service
            self.ansible_json['args'] = self.get_service_cmd
            self.ansible_json['module'] = 'shell'
            response = yield http_client(ansible_url, 'POST', self.cookie, self.ansible_json, 600)
        except HTTPError as err:
            gen_log.info(err)
            raise err
        else:
            result = json_decode(response.body)
            for key in result['msg'].keys():
                host = result['msg'][key]
                if host['status'] == 0:
                        services = list()
                        for service in host['msg'][0].split():
                            services.append(service)
                        host['msg'] = services
            raise Return(result)
















