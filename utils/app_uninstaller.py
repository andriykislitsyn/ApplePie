#!/usr/bin/python
from functools import wraps
from time import sleep

from lib.uninstaller import AppRemover, USER_LIB
from lib.privileged_helper import privileged_helper

APP_NAME = ''
BUNDLE_ID = ''

KEYCHAIN_ITEMS = ['%s.Service' % BUNDLE_ID]

USER_DATA = ['', '']

AGENTS = {'Agent': '%s/LaunchAgents/%s.Agent.plist' % (USER_LIB, BUNDLE_ID)}

SERVICES = {'Service': 'com.service.service'}

LEFTOVERS = ['', '']


def reload_helper(task):
    @wraps(task)
    def task_runner(*args, **kwargs):
        uninstaller.stop_application()
        [uninstaller.set_service_state(service, action='unload') for service in AGENTS.values()]
        sleep(0.5)
        task(*args, **kwargs)
        uninstaller.flush_preference_cache()
        [uninstaller.set_service_state(service, action='load') for service in AGENTS.values()]

    return task_runner


class AppUninstaller(AppRemover):
    def __init__(self):
        super(self.__class__, self).__init__('TestApp')

    @reload_helper
    def reset_application_state(self):
        [self.remove_filesystem_entry(item) for item in USER_DATA]
        [self.remove_keychain_entry(keychain_entry) for keychain_entry in KEYCHAIN_ITEMS]
        privileged_helper.execute('defaults delete %s' % BUNDLE_ID)

    def uninstall(self):
        self.save_diagnostics_data(search_pattern=self.name)
        self.stop_application()
        [self.set_service_state(service, action='remove') for service in AGENTS.values()]
        [self.set_service_state(service, action='remove', sudo=True) for service in SERVICES.values()]


uninstaller = AppUninstaller()
