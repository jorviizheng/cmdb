from __future__ import print_function

from tornado.testing import AsyncTestCase, AsyncHTTPClient,gen_test
from tornado.escape import json_encode

TEST_URL = "http://127.0.0.1:8083/ansible/task"
host = ['172.16.251.124']


class TempateTest(AsyncTestCase):

    @gen_test(timeout=60)
    def test_add(self):
        post_data = {
            'module': 'copy',
            'file_name': 'test',
            'host': host,
            'content': 'test',
            'dest': '/root/1',

        }

        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch(TEST_URL, method='POST', body=json_encode(post_data))
        print(response.body)
