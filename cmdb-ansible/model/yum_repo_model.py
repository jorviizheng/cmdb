from __future__ import print_function


class YumRepoModule:

    ansible_module_name = 'yum_repository'

    name = ''   #repos name
    state = ''
    description = ''
    enabled = ''
    gpgcheck = ''
    baseurl = ''

    def __init__(self, yum_repo_json):
        self.name = yum_repo_json['name']
        self.state = yum_repo_json['state']
        self.description = yum_repo_json['description']
        self.enabled = yum_repo_json['enabled']
        self.gpgcheck = yum_repo_json['gpgcheck']
        self.baseurl = yum_repo_json['baseurl']

    def yum_add_repo(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['args'] = 'name=%s description=%s enabled=%s gpgcheck=%s baseurl="%s"' %(
            self.name, self.description, self.enabled, self.gpgcheck, self.baseurl
        )
        task_dict['action'] = action_dict
        return task_dict

    def yum_remove_repo(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['args'] = 'name=%s state=%s' %(self.name, self.state)
        task_dict['action'] = action_dict
        return task_dict

