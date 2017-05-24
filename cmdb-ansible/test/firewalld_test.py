from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test, main

from tornado.escape import json_encode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
user_info = {
    'remote_user': 'root',
    'conn_pass': '123456'
}
host = ['172.16.251.101']

class FirewalldTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_port(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'zone': 'public',
            'immediate': 'true',
            'permanent': 'true',
            'state': 'enabled',
            'port': '8080/tcp',
            'module': 'firewalld'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_port_fail(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'zone': 'public',
            'immediate': 'true',
            'permanent': 'true',
            'state': 'enabled',
            'port': '8080/tccp',
            'module': 'firewalld'

        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_service(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'permanent': 'false',
            'state': 'enabled',
            'service': 'http',
            'immediate': 'false',
            'module': 'firewalld'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=60)
    def test_masquerade(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'permanent': 'true',
            'state': 'enabled',
            'masquerade': 'yes',
            'zone': 'public',
            'module': 'firewalld'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


