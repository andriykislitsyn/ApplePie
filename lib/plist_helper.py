from subprocess import check_output
import os
from time import sleep


class PlistHelper:
    """
    Data types: string, array, dict, bool, real, integer, date, data
    """
    def __init__(self, property_list):
        self.cli_helper = '/usr/libexec/PlistBuddy -c'
        self.plist = property_list

    def check_plist_presence(self):
        return os.path.isfile(self.plist)

    def create_plist(self):
        check_output('%s Save %s' % (self.cli_helper, self.plist))

    def read_plist_property(self, target_property=''):
        result = check_output('%s "Print :%s" %s' % (self.cli_helper, target_property, self.plist), shell=True)
        if 'Does Not Exist' in result:
            return None
        transformers = {'true': True, 'false': False}
        transformed_result = transformers.get(str(result))
        return transformed_result if transformed_result is not None else result

    def delete_plist_property(self, target_property, data_type=''):
        return check_output('%s "Delete :%s %s" %s' % (self.cli_helper, target_property,
                                                       data_type, self.plist), shell=True)

    def add_plist_property(self, target_property, payload):
        return check_output('%s "Add :%s %s" %s' % (self.cli_helper, target_property, payload, self.plist), shell=True)

    def set_plist_property(self, target_property, value):
        return check_output('%s "Set :%s %s" %s' % (self.cli_helper, target_property, value, self.plist), shell=True)

    @staticmethod
    def flush_preferences_cache():
        sleep(2)
        os.system('killall -u ${USER} cfprefsd')
