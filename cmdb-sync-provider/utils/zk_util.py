from kazoo.client import KazooClient
from kazoo.handlers.gevent import SequentialGeventHandler
from kazoo.exceptions import ConnectionLossException,NoAuthException,NoNodeError,ConnectionClosedError
from tornado.gen import coroutine,Return
from tornado.options import options
from tornado.log import gen_log

from operator import ne
import socket
import sys
sys.path.append('.')


import logging
logger = logging.getLogger('zk')
logger.setLevel(logging.ERROR)

class Zookeeper:

    def __init__(self, hosts):
        self.zk = KazooClient(hosts=hosts, handler=SequentialGeventHandler(), logger=logger)
        # returns immediately
        event = self.zk.start_async()

        # Wait for 30 seconds and see if we're connected
        event.wait(timeout=30)
        try:
            if not self.zk.connected:
                # Not connected, stop trying to connect
                self.zk.stop()
        except (ConnectionLossException, NoAuthException) as error:
            raise error
        except Exception as error:
            raise error

    @coroutine
    def get_children(self, node):
        try:
            children = self.zk.get_children_async(node)
            raise Return(children.get())
        except Exception as error:
            raise error

    @coroutine
    def get_node(self, node):
        try:
            data = self.zk.get_async(node)
            raise Return(data.get())
        except Exception as error:
            raise error

    @coroutine
    def check_path_exist(self, path):
        try:
            result = self.zk.exists(path)
            if result:
                raise Return(True)
            else:
                raise Return(False)
        except Exception as error:
            raise error

    @coroutine
    def create_path(self, path):
        try:
            result = self.zk.ensure_path_async(path)
            raise Return(result.get())
        except Exception as error:
            raise error

    @coroutine
    def create_node(self, path, value):
        try:
            result = self.zk.create_async(path=path, value=value,acl=None,ephemeral=True)
            raise Return(result.get())
        except Exception as error:
            raise error

    @coroutine
    def update_node(self, path,value,version=-1):
        try:
            result = self.zk.set_async(path,value,version)
            raise Return(result.get())
        except Exception as error:
            raise error

    @coroutine
    def update_node(self, path,value,version=-1):
        try:
            result = self.zk.set_async(path, value,version)
            raise Return(result.get())
        except Exception as error:
            raise error

    @coroutine
    def del_node(self, node):
        try:
            node_info = self.zk.delete_async(node)
            raise Return(node_info.get())
        except Exception as error:
            raise error

    def close(self):
        self.zk.stop()


@coroutine
def register():
    try:
        zk = KazooClient(hosts=options.zk_host,logger=logger)
        zk.start()

        try:
            if not zk.connected:
                # Not connected, stop trying to connect
                gen_log.error('no connected')
                zk.stop()
        except (ConnectionLossException, NoAuthException) as error:
            raise error
        except Exception as error:
            raise error
        else:
            host_ip = socket.gethostbyname(socket.gethostname())
            node_value = '%s:%s' % (host_ip, options.port)

            @zk.DataWatch(options.node_path)
            def watch_service(data, stat):
                if data is None:
                    gen_log.info('registry')
                    zk.create(path=options.node_path, value=node_value.encode('utf8'), acl=None, ephemeral=True)
    except Exception as err:
        gen_log.error(err)
        raise err