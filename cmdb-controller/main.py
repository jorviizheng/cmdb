#!/usr/bin/python3
from __future__ import print_function
from tornado.ioloop import IOLoop,PeriodicCallback
from tornado.gen import coroutine
from handler.task_handler import TaskHandler
from tornado.queues import Queue
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.options import define, options

from tornadis import ClientPool

from handler.check_handler import CheckHandler
from utils.zk_util import register


define("queue_count", default=10, help='Queue Max Number', type=int)
define("port", default=8082, help='Controller Web', type=int)
define("zk_host", default='172.16.251.33:2181', help='Zookeeper Server', type=str)
define("node_path", default='/cmdb/service/controller', help='Controller Service Root', type=str)
define("ansible_node_path", default='/cmdb/service/ansible', help='Ansible Service Root', type=str)
define("async_api_node_path", default='/cmdb/service/async_api', help='Async Api Service Root', type=str)
define("provision_node_path", default='/cmdb/service/provision', help='Provision Service', type=str)
define("date_fmt", default='%Y-%m-%d %H:%M:%S', help='data time', type=str)

define("redis_host", default='172.16.251.33', type=str)
define("redis_session_db", default=7, type=int)
define("redis_yum_source_db", default=8, type=int)
define("redis_server_db", default=9, type=int)
define("redis_port", default=6379, type=int)

define("session_expire_time", default=36000, type=int)

define("service_user", default='admin', help='user', type=str)


queue = Queue(maxsize=options.queue_count)

async_session_pool = ClientPool(max_size=100,
                                     client_timeout=30,
                                     host=options.redis_host,
                                     port=options.redis_port,
                                     db=options.redis_session_db,
                                     autoconnect=True)


@coroutine
def new_task():
    task = TaskHandler(queue, async_session_pool)
    IOLoop.current().spawn_callback(task.consumer)
    yield task.new_task()     # Wait for producer to put all tasks.

@coroutine
def check_task():
    task = TaskHandler(queue, async_session_pool)
    IOLoop.current().spawn_callback(task.consumer)
    yield task.check_task()     # Wait for producer to put all tasks.


if __name__ == "__main__":
    options.logging = 'info'
    options.parse_command_line()

    settings = {
        "cookie_secret": "61oEdfTzKXdQAGaYddkL5fgEdf123mGeJJFfusYh7EQnp2fXdTP1o/Vo=",
        'login_url':'/login.html',
        'xsrf_cookies': False,
        'max_age_days': 0.1
    }
    app = Application(
        handlers=[
            (r'/controller/status', CheckHandler),
        ],
        debug=True,
        **settings
    )

    PeriodicCallback(new_task, 10000).start()
    PeriodicCallback(check_task, 60000).start()
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().run_sync(register)
    IOLoop.instance().start()

