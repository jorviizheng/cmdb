from __future__ import print_function
from tornado.httpclient import AsyncHTTPClient,HTTPError,HTTPClient
from tornado.log import gen_log
from tornado.httputil import HTTPHeaders
from tornado.gen import coroutine,Return
from tornado.escape import json_decode, json_encode
import re
import json


class Ilo4Util():

    auth_url = 'redfish/v1/sessions/'
    mac_addr_url ='rest/v1/Systems/1/NetworkAdapters/1'
    SESSTION_LOCATION = 'Location'
    SESSION_X_AUTH_TOKEN = 'X-Auth-Token'

    uefi_boot_url = 'rest/v1/Systems/1'
    boot_selection = 'IPv4'

    uefi_target_boot_source_override_supported = 'UefiTargetBootSourceOverrideSupported'
    uefi_target_boot_source_override_option = 'UefiTargetBootSourceOverride'


    reset_url = 'rest/v1/Systems/1'
    reset_json = {"Action":"Reset","ResetType":"ForceRestart"}

    ilo4_host = ''
    user_name = ''
    user_password = ''

    sessions = {}

    def __init__(self,host,user_name,user_password):
        self.ilo4_host = host
        self.user_name = user_name
        self.user_password = user_password
        self.sessions = self.get_session()


    def get_session(self):
        fetch_url = 'https://%s/%s' % (self.ilo4_host, self.auth_url)
        post_data = json.dumps({"UserName": self.user_name, "Password": self.user_password})
        http_client = HTTPClient()
        headers = HTTPHeaders()
        headers.add('Content-Type', 'application/json')
        try:
            response = http_client.fetch(
                fetch_url,
                method='POST',
                headers=headers,
                validate_cert=False,
                body=post_data)
        except HTTPError as error:
            gen_log.error('ILO4 %s session error:%s' % (self.ilo4_host,error))
            raise error
        else:
            sessions = {
                self.SESSTION_LOCATION: response.headers['Location'],
                self.SESSION_X_AUTH_TOKEN: response.headers['X-Auth-Token']
            }
            return sessions

    def __del__(self):
        http_client = HTTPClient()
        headers = HTTPHeaders()
        headers.add(self.SESSTION_LOCATION, self.sessions[self.SESSTION_LOCATION])
        headers.add(self.SESSION_X_AUTH_TOKEN, self.sessions[self.SESSION_X_AUTH_TOKEN])

        fetch_url ='%s' % self.sessions[self.SESSTION_LOCATION]
        try:
            response = http_client.fetch(
                fetch_url,
                headers=headers,
                method='DELETE',
                validate_cert=False
            )
            return response
        except HTTPError as error:
            raise error

    @coroutine
    def get_response(self, url, method,headers=None, body=None):
        http_client = AsyncHTTPClient()

        headers = HTTPHeaders()
        headers.add(self.SESSTION_LOCATION,self.sessions[self.SESSTION_LOCATION])
        headers.add(self.SESSION_X_AUTH_TOKEN,self.sessions[self.SESSION_X_AUTH_TOKEN])

        if method == 'PATCH' or method == 'POST':
            headers.add('Content-Type', 'application/json')
        try:
            response = yield http_client.fetch(
                url,
                headers=headers,
                method=method,
                validate_cert=False,
                body=body)
        except HTTPError as error:
            raise error
        else:
            raise Return(response)

    @coroutine
    def get_mac_address(self):
        fetch_url = 'https://%s/%s' % (self.ilo4_host, self.mac_addr_url)
        try:
            response = yield self.get_response(fetch_url, 'GET')
        except HTTPError as error:
            gen_log.error('Get %s mac address error: %s'% (self.ilo4_host, error))
            raise error
        else:
            mac_addr_list = []
            result = json_decode(response.body)
            for port in result['PhysicalPorts']:
                port_status = port['Status']['State']
                port_health = port['Status']['Health']
                mac_addr = port['MacAddress']
                if port_status == 'Enabled' and port_health == 'OK':
                    mac_addr_list.append(mac_addr)

            if len(mac_addr_list) == 0:
                raise ("%s no mac could be used" % self.ilo4_host)

            mac_addr_dict = dict()
            for index in range(len(mac_addr_list)):
                key_name = "mac%s" % index
                mac_addr_dict[key_name] = mac_addr_list[index]
            raise Return(mac_addr_dict)

    @coroutine
    def get_uefi_boot_json(self):
        boot_json = dict()
        fetch_url = 'https://%s/%s' % (self.ilo4_host, self.uefi_boot_url)
        try:
            response = yield self.get_response(fetch_url, 'GET')
            result = json_decode(response.body)
        except HTTPError as error:
            gen_log.error('Get %s Boot Json Error: %s'% (self.ilo4_host,error))
            raise error
        else:
            result = json_decode(response.body)
            for boot_option in result['Boot'][self.uefi_target_boot_source_override_supported]:
                if re.search(self.boot_selection, boot_option):
                    boot_json["Boot"] = dict()
                    boot_json["Boot"][self.uefi_target_boot_source_override_option] = boot_option
            raise Return(boot_json)

    @coroutine
    def change_boot_temporary(self):
        boot_json = yield self.get_uefi_boot_json()
        fetch_url = 'https://%s/%s' % (self.ilo4_host, self.uefi_boot_url)
        try:
            response = yield self.get_response(fetch_url, 'PATCH', body=json_encode(boot_json))
        except HTTPError as error:
            gen_log.error('Change %s boot error: %s' % (self.ilo4_host,error))
            raise error
        else:
            result = json_decode(response.body)
            gen_log.info('Change Boot %s :%s' % (self.ilo4_host, result['Messages'][0]['MessageID']))
            raise Return(0)


    @coroutine
    def reset_server(self):
        fetch_url = 'https://%s/%s' % (self.ilo4_host,self.reset_url)
        try:
            response = yield self.get_response(fetch_url,'POST',body=json.dumps(self.reset_json))
        except HTTPError as error:
            gen_log.error('Reset %s Error:%s' %(self.ilo4_host, error))
            raise error
        else:
            result = json_decode(response.body)
            gen_log.info('Reset %s :%s' % (self.ilo4_host, result['Messages'][0]['MessageID']))
            raise Return(0)



    @coroutine
    def get_detail(self):
        fetch_url = 'https://%s/%s' % (self.ilo4_host, 'rest/v1/Systems/1')
        response = None
        try:
            response = yield self.get_response(fetch_url,'GET')
        except Exception as ex:
            raise ex
        else:
            return_body = {}
            if response.code == 200:
                # return_body['status'] = response.code
                # return_body['Body'] = json_decode(response.body)
                # return return_body
                detail = json_decode(response.body)
                for key in detail.keys():
                    print('key:%s,value:%s' %(key,detail[key] ))
            else:
                print(response)
                # return_body['status'] = response.code
                # return_body['Body'] = response
                # return return_body

# @coroutine
# def main():
#     client = Ilo4Util('172.16.250.24','admin','password')
#     result =yield client.reset_server()
#     print(result)
#
# if __name__ == '__main__':
#     io_loop = IOLoop.current()
#     io_loop.run_sync(main)
    # @coroutine
    # def get(self, *args, **kwargs):
    #     if len(args) == 0:
    #         self.write('2')
    #     elif args[0] == 'mac':
    #         self.set_ilo4_info()
    #         self.write('mac')
    #     else:
    #         self.write('1')

    # @tornado.gen.coroutine
    # def post(self, *args, **kwargs):
    #     if len(args) == 0:
    #         self.write('2')
    #     elif args[0] == 'getMacAddress':
    #         self.set_ilo4_info()
    #         result = yield self.get_macaddress()
    #         self.write(result)
    #     elif args[0] == 'setTemporaryBoot':
    #         self.set_ilo4_info()
    #         response = yield self.change_boot_temporary()
    #         return_body = {}
    #         return_body['status'] = response.code
    #         return_body['Body'] = json.loads(response.body)
    #         self.write(return_body)
    #     else:
    #         self.write('1')
