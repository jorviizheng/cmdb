from __future__ import print_function


class HostnameModel(object):

    def __init__(self, ansible_json):
        self.ansible_module_name = 'hostname'
        self.host_name = ansible_json['host_name']

    def create_task(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['name'] = self.host_name
        task_dict['action'] = action_dict
        return task_dict


