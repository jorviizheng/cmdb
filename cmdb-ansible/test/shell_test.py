from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode,json_decode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
user_info = {
    'remote_user': 'root',
    'conn_pass': '123456'
}
host = ['172.16.251.102','172.16.251.123','172.16.251.33']
# host = ['172.16.251.123','172.16.251.33']


class UserTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_shell(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'shell',
            'args': 'yum list installed |grep httpd',

        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=60)
    def test_ststderrderrshell_get_user(self):
        post_data = {
            # 'user_info': json_encode(user_info),
            'host': host,
            'module': 'shell',
            'args': 'hostname1',

        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)
        result = json_decode(response.body)
        print(result)
        # for item in result['msg']:
        #     print(item)