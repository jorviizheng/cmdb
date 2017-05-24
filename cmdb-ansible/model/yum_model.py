from __future__ import print_function

class YumModule:

    ansible_module_name = 'yum'

    name = ''   #install service names like  gcc or gcc,openssl
    list = ''
    disable_gpg_check = ''
    state = ''
    update_cache = False
    validate_certs = True
    exclude = ''
    disablerepo = ''

    def __init__(self, yum_json):
        if isinstance(yum_json['package_name'], list):
            self.name = ','.join(yum_json['package_name'])
        else:
            self.name = yum_json['package_name']

        self.state = yum_json['state']
        self.list = None
        self.disable_gpg_check = False
        self.update_cache = False
        self.validate_certs = True
        self.exclude = None
        self.disablerepo = None

    def yum_task(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['args'] = 'name=%s state=%s' % (self.name, self.state)
        task_dict['action'] = action_dict
        return task_dict


