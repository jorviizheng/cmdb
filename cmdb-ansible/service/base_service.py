from __future__ import print_function

import sys
import re
sys.path.append('.')
from tornado.gen import coroutine, Return
from tornado.log import gen_log
from tornado.escape import json_decode
from utils.ansible_util import AnsibleUtil


class BaseService(object):
    
    def __init__(self, ansible_json):
        self.ansible_json = ansible_json
        self.user_info = json_decode(ansible_json['user_info']) if 'user_info' in ansible_json \
            else {'remote_user': 'root'}
        self.host = ansible_json['host']
        self.ansible_json = ansible_json
        self.result_json = dict()

    def return_json(self, code, msg):
        return_json = dict()
        return_json['status'] = code
        return_json['msg'] = msg
        return return_json

    @coroutine
    def run(self, play_tasks_list):
        print(self.ansible_json)
        play = AnsibleUtil(self.host, self.user_info, play_tasks_list)
        try:
            code = yield play.run_ansible()
        except Exception as ex:
            gen_log.error(ex)
            raise ex
        else:
            result_detail_dict = play.get_result()
            print(result_detail_dict)
            for key in result_detail_dict.keys():
                result_detail_dict[key] = result_detail_dict[key].replace('\\n', '').replace('\\r', '').replace('\\t', '')
                result_detail_dict[key] = json_decode(result_detail_dict[key])
                gen_log.info(result_detail_dict[key])
            raise Return(self.return_json(code, result_detail_dict))