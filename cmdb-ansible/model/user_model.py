from __future__ import print_function


class UserModel(object):

    def __init__(self, user_json):
        self.ansible_module_name = 'user'

        #用户名
        self.name = user_json['name']

        #操作
        self.state = user_json['state']

        #密码
        self.password = user_json['password'] if 'password' in user_json else None

        #组
        self.group = user_json['group'] if 'group' in user_json else None

        #多个组
        self.groups = user_json['groups'] if 'groups' in user_json else None

        #说明
        self.comment = user_json['comment'] if 'comment' in user_json else 'Ansible Create'

        #是否添加/home目录
        self.create_home = user_json['create_home'] if 'zone' in user_json else 'yes'

        #强制执行
        self.force = user_json['force'] if 'force' in user_json else 'no'

        #是否为系统用户
        self.system = user_json['system'] if 'system' in user_json else 'no'

        #修改密码
        self.update_password = None

        if 'update_password' in user_json:
            if user_json['update_password'] == 'yes':
                self.update_password = 'always'



    #添加用户
    def add_user(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['name'] = self.name

        if self.group:
            action_dict['group'] = self.group

        if self.groups:
            action_dict['groups'] = self.groups

        action_dict['password'] = self.password

        action_dict['state'] = self.state

        action_dict['createhome'] = self.create_home
        action_dict['system'] = self.system

        task_dict['action'] = action_dict
        return task_dict


    #删除用户
    def del_user(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['name'] = self.name
        action_dict['state'] = self.state
        action_dict['force'] = self.force

        task_dict['action'] = action_dict
        return task_dict


    #更新密码
    def change_password(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['name'] = self.name
        action_dict['password'] = self.password
        if self.update_password:
            action_dict['update_password'] = self.update_password
        else:
            raise Exception('update password args error, no update_password:update')
        task_dict['action'] = action_dict
        return task_dict
