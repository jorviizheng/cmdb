from tornadis import ClientPool, TornadisException
from tornado.gen import coroutine, Return
from tornado.escape import json_decode, json_encode
import redis


class AsyncRedisUtil:

    def __init__(self,pool):
        self.pool = pool
        self.client = self.pool.get_client_nowait()

    @coroutine
    def keys(self, key):
        try:
            result = yield self.client.call('keys',key)
        except TornadisException as error:
            raise error
        else:
            raise Return(len(result))

    @coroutine
    def get(self, key):
        try:
            result = yield self.client.call('get', key)
        except TornadisException as error:
            raise error
        else:
            result = json_decode(result)
            raise Return(result)

    @coroutine
    def set(self, key, value):
        try:
            value = json_encode(value)
            result = yield self.client.call('set', key, value)
        except TornadisException as error:
            raise error
        else:
            raise Return(result)

    @coroutine
    def delete(self, key):
        try:
            result = yield self.client.call('del', key)
        except TornadisException as error:
            raise error
        else:
            raise Return(result)

    @coroutine
    def expire(self, key, time):
        try:
            result = yield self.client.call('EXPIRE', key, time)
        except TornadisException as error:
            raise error
        else:
            raise Return(result)

    def __del__(self):
        self.pool.release_client(self.client)


class SyncRedisUtil:
    def __init__(self, pool):
        self.pool = pool
        self.client = redis.Redis(connection_pool=self.pool)

    def key_exist(self, key):
        exist = self.client.keys(key)
        if len(exist) == 0:
            return False
        return True


