from __future__ import print_function
import sys
sys.path.append('.')


class CopyModel(object):

    def __init__(self, copy_json):
        try:
            self.ansible_module_name = 'copy'
            self.file_name = copy_json['file_name']
            self.content = copy_json['content']
            self.dest = copy_json['dest'] + '/' + self.file_name
            self.owner = copy_json['owner'] if 'owner' in copy_json else 'root'
            self.group = copy_json['group'] if 'group' in copy_json else 'root'
            self.mode = copy_json['mode'] if 'mode' in copy_json else '0644'
            self.backup = copy_json['backup'] if 'backup' in copy_json else 'no'
        except Exception as err:
            print(err)


    def create_task(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['content'] = self.content
        action_dict['dest'] = self.dest
        action_dict['owner'] = self.owner
        action_dict['group'] = self.group
        action_dict['mode'] = self.mode
        action_dict['backup'] = self.backup
        task_dict['action'] = action_dict
        return task_dict


