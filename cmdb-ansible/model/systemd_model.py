from __future__ import print_function


STARTED = 'started'
STOPPED = 'stopped'
RESTARTED = 'restarted'
RELOADED = 'reloaded'


class SystemdModel(object):

    def __init__(self, systemd_json):
        self.ansible_module_name = 'systemd'
        self.name = systemd_json['name']
        self.state = systemd_json['state']
        self.enabled = systemd_json['enabled'] if 'enabled 'in systemd_json else 'yes'
        self.daemon_reload = systemd_json['daemon_reload'] if 'daemon_reload 'in systemd_json else 'yes'

    # masquerade = yes or no
    def systemd_task(self):
        task_dict = dict()
        action_dict = dict()
        action_dict['module'] = self.ansible_module_name
        action_dict['name'] = self.name
        action_dict['daemon_reload'] = self.daemon_reload
        action_dict['enabled'] = self.enabled
        action_dict['state'] = self.state
        task_dict['action'] = action_dict
        return task_dict