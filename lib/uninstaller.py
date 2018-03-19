__version__ = '2017.09.05'

from os import environ, path, system, unlink
from platform import mac_ver
import re
from shutil import rmtree
from subprocess import check_output
from tempfile import gettempdir

from config import admin_password
from lib.privileged_helper import privileged_helper

# System constants
ADMIN_PASSWORD = admin_password
MACOS_VERSION = re.search('\d{2}.\d*', mac_ver()[0]).group()
# Directories
DIAGNOSTICS_DATA = '/Library/Logs/DiagnosticReports'
HOME = environ['HOME']
USER_LIB = HOME + '/Library'
TMP_DIR = gettempdir()


class AppRemover(object):
    def __init__(self, application_name):
        self.name = application_name

    def __enter__(self):
        system('echo "%s" | sudo -S -v -p ""' % ADMIN_PASSWORD)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        system('sudo -k')

    def stop_application(self, application=None, agent=None):
        self.kill_process_by_name(self.name if application is None else application)
        if agent is not None:
            self.set_service_state(agent, action='unload')

    def start_helper(self, helper):
        self.flush_preference_cache()
        self.set_service_state(helper, action='load')

    @staticmethod
    def set_service_state(agent, action, sudo=False):
        """ Set a target state for a specified agent/daemon.
            :param str agent: Target agent
            :param str action: Common actions: load, unload, remove.
            :param bool sudo: Elevate user rights. """
        if sudo:
            return privileged_helper.execute('launchctl {0} {1}'.format(action, agent))
        return system('launchctl {0} {1}'.format(action, agent))

    def remove_keychain_entry(self, keychain_entry, flag='s'):
        self.execute_silently('security delete-generic-password -{0} "{1}"'.format(flag, keychain_entry))

    def delete_keychain(self, keychain):
        self.execute_silently('security delete-keychain "{0}/Library/Keychains/{1}.keychain"'.format(HOME, keychain))

    def flush_preference_cache(self):
        self.kill_process_by_name('cfprefsd')

    def kill_process_by_name(self, process_name):
        self.execute_silently('killall ${{USER}} "{}"'.format(process_name))

    def clear_application_services(self, search_pattern):
        processes_list = check_output(['launchctl', 'list'])
        for process in filter(lambda x: x.startswith(search_pattern), processes_list.split()):
            self.set_service_state('remove', str(process))

    @staticmethod
    def save_diagnostics_data(search_pattern, destination=path.join(HOME, 'Desktop')):
        diagnostics_reports = '%s/*%s*' % (DIAGNOSTICS_DATA, search_pattern)
        privileged_helper.execute('mv "{0}" "{1}"'.format(diagnostics_reports, destination))

    def remove_filesystem_entry(self, filesystem_entry):
        if not path.exists(filesystem_entry):
            return
        if filesystem_entry.startswith('/Library/') and len(filesystem_entry.split('/')) < 4:
            return  # A system folder is selected to be removed.
        filesystem_entry_type = 'dir_' if path.isdir(filesystem_entry) else 'file_'
        domain = 'user' if filesystem_entry.startswith(HOME) else 'sys'
        filesystem_entry_type += domain
        remove_filesystem_entry = {'dir_sys': self.remove_system_folder,
                                   'dir_user': rmtree,
                                   'file_sys': self.remove_system_file,
                                   'file_user': unlink
                                   }.get(filesystem_entry_type)
        try:
            remove_filesystem_entry(filesystem_entry)
        except OSError:
            print('Requested resource: "%s" cannot be removed')

    @staticmethod
    def remove_system_file(file_path):
        return privileged_helper.execute('rm -f "{0}"'.format(file_path))

    @staticmethod
    def remove_system_folder(folder_path):
        return privileged_helper.execute('rm -rf "{0}"'.format(folder_path))

    @staticmethod
    def execute_silently(command):
        return system('%s >/dev/null 2>&1' % command)
