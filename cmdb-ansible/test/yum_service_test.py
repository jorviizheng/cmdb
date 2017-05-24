from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
user_info = {
    'remote_user': 'root',
    'conn_pass': '123456'
}
host = ['172.16.251.101']
package = ['httpd']

class YumRepoTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_add(self):
        post_data = {
            'user_info': json_encode(user_info),
            'module': 'yum',
            'host': host,
            'package_name': package,
            'state': 'present'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_del(self):
        post_data = {
            'user_info': json_encode(user_info),
            'module': 'yum',
            'host': host,
            'package_name': package,
            'state': 'absent'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)