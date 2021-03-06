__author__ = 'pippo'
from paramiko import SSHClient,AutoAddPolicy
from tornado.ioloop import IOLoop
from tornado.gen import coroutine,Return

class Ssh:

    _ssh = None
    _user_name = 'root'
    _user_password = '123123'
    _host = None
    _port = 22
    _default_cmd = 'date'

    def __init__(self, host):
        self._host = host
        self._ssh = SSHClient()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())

    @coroutine
    def ssh_connnect(self):
        try:
            self._ssh.connect(self._host, self._port, self._user_name,
                              self._user_password,timeout=1)
            stdin, stdout, stderr = self._ssh.exec_command(self._default_cmd)
        except Exception as e:
            raise Return(1)
        else:
            raise Return(0)

    def __del__(self):
        self._ssh.close()


@coroutine
def main():
    ssh = Ssh('172.16.251.24')
    result = yield ssh.ssh_connnect()
    print(result)



if __name__ == "__main__":
    #main()
    io_loop = IOLoop.current()
    io_loop.run_sync(main)
