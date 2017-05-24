from tornado.options import options
from tornado.gen import coroutine, Return
import hashlib
import sys
sys.path.append('.')
from utils.api_redis import AsyncRedisUtil


class SessionUtil(object):
    def __init__(self, session_id, redis_pool):
        self._id = session_id
        self._redis = AsyncRedisUtil(redis_pool)

    def __create_key(self):
        session_md5 = hashlib.md5()
        session_md5.update(self._id)
        value = session_md5.hexdigest()
        return value

    @coroutine
    def exist_session(self):
        exist = yield self._redis.keys(self._id)
        raise Return(exist)

    @coroutine
    def get_session(self):
        session = yield self._redis.get(self._id)
        raise Return(session)

    @coroutine
    def set_session(self):
        session_value = self.__create_key()
        yield self._redis.set(self._id, session_value)
        yield self._redis.expire(self._id, options.session_expire_time)

    @coroutine
    def del_session(self):
        exist = yield  self.exist_session()
        if exist > 0:
            yield self._redis.delete(self._id)