from xmlrpc import client
from tornado.gen import coroutine,Return
from tornado.log import gen_log
from tornado.ioloop import IOLoop


class CobberUtil:
    cobbler_url = '/cobbler_api'
    # cobbler_host = ''
    user_name = 'admin'
    user_passwd = 'password'
    client = None
    token = None


    server_name = ''
    mac_address = ''
    server_ip = ''
    profile = ''

    def __init__(self, cobbler_host, server_name, mac_addr, server_ip, profile):
        self.cobbler_url = 'http://'+cobbler_host+self.cobbler_url
        self.client = client.ServerProxy(self.cobbler_url)
        self.token = self.client.login(self.user_name, self.user_passwd)

        self.server_name = server_name
        self.mac_address = mac_addr
        self.server_ip = server_ip
        self.profile = profile


    @coroutine
    def add_cobbler(self):
        result = 1
        try:
            check_result = yield self.check_system_exist()
            if check_result != 1: # old system exist
                remove_result = yield self.del_old_system(check_result[0])
                if remove_result > 0:
                    raise Return(remove_result)
            result = yield self.add_new_system()
        except client.Fault as fault:
            raise Return(fault.faultCode)
        else:
            raise Return(result)

    @coroutine
    def add_new_system(self):
        try:
            system_id = self.client.new_system(self.token)
            self.client.modify_system(system_id, "name", self.server_name, self.token)
            self.client.modify_system(system_id, "hostname", self.server_name, self.token)
            #bind mac address and ip
            self.client.modify_system(system_id, 'modify_interface', {
                "macaddress-eth0": self.mac_address,
                "ipaddress-eth0": self.server_ip,
            }, self.token)

            #bind cobbler profile
            self.client.modify_system(system_id, "profile", self.profile, self.token)

            self.client.save_system(system_id, self.token)
            self.client.sync(self.token)
        except client.Fault as fault:
            gen_log.error('Cobbler add new system error:%s' % fault)
            raise fault
        else:
            raise Return(0)

    @coroutine
    def del_old_system(self,hostname):
        try:
            self.client.remove_system(hostname, self.token)
            self.client.sync(self.token)
        except client.Fault as fault:
            gen_log.error('Cobbler del old system error:%s' % fault)
            raise Return(fault.faultCode)
        else:
            raise Return(0)

    @coroutine
    def check_system_exist(self):
        try:
            systems = self.client.find_system({"mac_address": self.mac_address})
        except client.Fault as fault:
            gen_log.error('get mac error:%s' % fault)
            raise Return(fault.faultCode)
        else:
            if len(systems) > 0:
                raise Return(systems)
            else:
                raise Return(1)

#
# @coroutine
# def main():
#     cobbler = CobblerService('172.16.251.30','slave23','1c:98:ec:2f:3d:58','172.16.251.24','centos7.0-x86_64')
#     #yield cobbler.add_new_system()
#     check = yield cobbler.check_system_exist()
#     print(check)
#     # if check != 1:
#     #     result = yield cobbler.del_old_system()
#     # print(result)
#
#
#
#
# if __name__ == '__main__':
#     io_loop = IOLoop.current()
#     io_loop.run_sync(main)
