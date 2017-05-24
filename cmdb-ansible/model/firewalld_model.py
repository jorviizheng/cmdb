from __future__ import print_function


class FirewalldModel(object):

    def __init__(self, firewall_json):
        self.ansible_module_name = 'firewalld'
        self.firewall_json = firewall_json
        self.zone = firewall_json['zone'] if 'zone' in firewall_json else 'public'
        #添加的规则是否立即生效
        self.immediate = firewall_json['immediate'] if 'immediate' in firewall_json else 'true'
        #永久生效
        self.permanent = firewall_json['permanent'] if 'permanent' in firewall_json else 'true'

    #service like httpd
    def firewall_service(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['immediate'] = self.immediate
        action_dict['service'] = self.firewall_json['service']
        action_dict['permanent'] = self.permanent
        action_dict['state'] = self.firewall_json['state']
        action_dict['zone'] = self.zone
        task_dict['action'] = action_dict
        return task_dict

    #port like 8080/tcp, 8080-8081/tcp
    #state = enabled or disabled
    def firewall_port(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['immediate'] = self.immediate
        action_dict['port'] = self.firewall_json['port']
        action_dict['permanent'] = self.permanent
        action_dict['state'] = self.firewall_json['state']
        action_dict['zone'] = self.zone
        task_dict['action'] = action_dict
        return task_dict


    # source like  192.168.1.0/24
    def firewall_source(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['immediate'] = self.immediate
        action_dict['source'] = self.firewall_json['source']
        action_dict['permanent'] = self.permanent
        action_dict['state'] = self.firewall_json['state']
        action_dict['zone'] = self.zone
        task_dict['action'] = action_dict
        return task_dict


    # masquerade = yes or no
    def firewall_masquerade(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['immediate'] = self.immediate
        action_dict['masquerade'] = self.firewall_json['masquerade']
        action_dict['permanent'] = self.permanent
        action_dict['state'] = self.firewall_json['state']
        action_dict['zone'] = self.zone
        task_dict['action'] = action_dict
        return task_dict