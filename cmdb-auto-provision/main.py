#!/usr/bin/python3
from __future__ import print_function
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from tornadis import ClientPool
from redis import ConnectionPool

from utils.zk_util import register

from tornado.options import define, options

from handler import provision_handler
from handler import hardware_handler

define("port", default=8085, help='listen port', type=int)
define("zk_host", default='172.16.251.33:2181', help='Zookeeper Server', type=str)
define("node_path", default='/cmdb/service/provision', help='provision Service Root', type=str)
define("async_api_node_path", default='/cmdb/service/async_api', help='Async Api Service Root', type=str)
define("ansible_node_path", default='/cmdb/service/ansible', help='Ansible Service Root', type=str)

define("redis_host", default='172.16.251.33', type=str)
define("redis_session_db", default=7, type=int)
define("redis_yum_source_db", default=8, type=int)
define("redis_server_db", default=9, type=int)
define("redis_port", default=6379, type=int)

define("session_expire_time", default=36000, type=int)

define("service_user", default='admin', help='user', type=str)


HANDLERS =[provision_handler, hardware_handler]


class App(Application):
    def __init__(self, debug=False):
        settings = {
            "cookie_secret": "61oEdfTzKXdQAGaYddkL5fgEdf123mGeJJFfusYh7EQnp2fXdTP1o/Vo=",
            'login_url':'/login.html',
            'xsrf_cookies': False,
            'max_age_days': 0.1,
            'expires':600,
            'debug': debug,
        }
        handles = []

        self.sync_session_pool = ConnectionPool(
            max_connections=10,
            host=options.redis_host,
            port=options.redis_port,
            db=options.redis_session_db)

        self.async_session_pool = ClientPool(max_size=100,
                        client_timeout=30,
                        host=options.redis_host,
                        port=options.redis_port,
                        db=options.redis_session_db,
                        autoconnect=True)

        super(App, self).__init__(handles, **settings)

    def load_handler_module(self, handler_module, perfix = ".*$"):
        """
        从模块加载 RequestHandler
            `handler_module` : 模块
            `perfix` : url 前缀
        """
        # 判断是否是有效的 RequestHandler (是类且是 RequestHandler 的子类)
        is_handler = lambda cls: isinstance(cls, type) \
                     and issubclass(cls, RequestHandler)
        # 判断是否拥有 url 规则
        has_pattern = lambda cls: hasattr(cls, 'url_pattern') \
                      and cls.url_pattern
        handlers = []
        # 迭代模块成员
        for i in dir(handler_module):
            cls = getattr(handler_module, i)
            if is_handler(cls) and has_pattern(cls):
                handlers.append((cls.url_pattern, cls))
        self.add_handlers(perfix, handlers)

    def _get_host_handlers(self, request):
        """
        覆盖父类方法, 一次获取所有可匹配的结果. 父类中该方法一次匹配成功就返回, 忽略后续
        匹配结果. 现通过使用生成器, 如果一次匹配的结果不能使用可以继续匹配.
        """
        host = request.host.lower().split(':')[0]
        # 使用生成器表达式而非列表推导式, 减少性能折扣
        handlers = (i for p, h in self.handlers for i in h if p.match(host))
        # Look for default host if not behind load balancer (for debugging)
        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]
        return handlers

if __name__ == "__main__":
    options.parse_command_line()
    app = App(debug=True)

    for handler in HANDLERS:
        app.load_handler_module(handler)

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().run_sync(register)
    IOLoop.instance().start()


