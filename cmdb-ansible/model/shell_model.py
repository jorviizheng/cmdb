from __future__ import print_function

class ShellModel(object):

    ansible_module_name = 'shell'
    args = ''
    chdir = ''
    creates = ''
    executable = ''
    free_form = ''
    removes = False
    warn = True

    def __init__(self, shell_json):
        self.args = shell_json['args']
        self.chdir = None
        self.creates = None
        self.executable = None
        self.free_form = None
        self.removes = None
        self.warn = None

    def create_task(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['args'] = self.args
        task_dict['action'] = action_dict
        return task_dict


# if __name__ == '__main__':
#     yum = YumModule(['gcc','openssl'],'present')
#     print(yum.yum_list_package())


