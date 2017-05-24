from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
user_info = {
    'remote_user': 'root',
    'conn_pass': '123456'
}
host = ['172.16.251.101']
package = ['gcc']

class YumRepoTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_add(self):
        post_data = {
            'user_info': json_encode(user_info),
            'module': 'yum_repo',
            'host': host,
            'name': 'wanda',
            'state': 'present',
            'description': 'local',
            'enabled': '1',
            'gpgcheck': '0',
            'baseurl': 'http://yum.wanda.cn'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)


    @gen_test(timeout=60)
    def test_del(self):
        post_data = {
            'user_info': json_encode(user_info),
            'module': 'yum_repo',
            'host': host,
            'name': 'wanda',
            'state': 'absent',
            'description': 'local',
            'enabled': '1',
            'gpgcheck': '0',
            'baseurl': 'http://yum.wanda.cn'
        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)