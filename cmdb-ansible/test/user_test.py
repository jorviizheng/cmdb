from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
user_info = {
    'remote_user': 'root',
    'conn_pass': '123456'
}
host = ['172.16.251.101']


from passlib.hash import sha512_crypt

password = sha512_crypt.using(rounds=5000).hash('123123')


class UserTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_add_user(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'absent',
            'name': 'test1',
            'password': password
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_update_passwd(self):
        new_passwd = sha512_crypt.using(rounds=5000).hash('milan')
        print(new_passwd)
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'name': 'test2',
            'state': 'update',
            'password': new_passwd,
            'update_password': 'yes'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_add_user_group(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'present',
            'name': 'test2',
            'password': password,
            'group': 'test2'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=60)
    def test_add_user_groups(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'present',
            'name': 'test3',
            'password': password,
            'groups': 'test2,root'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_del_user_test1(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'absent',
            'name': 'test2',
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=60)
    def test_del_user(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'present',
            'name': 'test2',
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)

    @gen_test(timeout=60)
    def test_del_user_force(self):
        post_data = {
            'user_info': json_encode(user_info),
            'host': host,
            'module': 'user',
            'state': 'present',
            'name': 'test3',
            'force': 'yes'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)