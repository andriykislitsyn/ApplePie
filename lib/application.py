import os

from lib.applescript_helper import AppleScriptHelper
from lib.condition import wait_for
from lib.plist_helper import PlistHelper


class Application:
    def __init__(self, app_name):
        self.name = app_name
        self.application_plist = '/Applications/"%s".app/Contents/Info.plist'
        self.contents_reader = PlistHelper(self.application_plist % self.name)
        self.applescript_helper = AppleScriptHelper(self.name)

    def _get_version(self):
        return self.contents_reader.read_plist_property('CFBundleShortVersionString')

    def _get_build(self):
        return self.contents_reader.read_plist_property('CFBundleVersion')

    def relaunch(self):
        self.quit()
        self.launch()

    def quit(self):
        os.system('killall -u ${{USER}} "{0}"'.format(self.name))
        return wait_for(self.assert_quit, 10)

    def launch(self):
        self.activate()
        return self.frontmost

    def activate(self):
        self.applescript_helper.tell_application('activate')

    def assert_quit(self):
        return self.name not in self.applescript_helper.get_processes_list()

    def _assert_launched(self):
        return self.name in self.applescript_helper.get_processes_list()

    def close_windows(self):
        self.applescript_helper.tell_application_process('close every window')

    def close_documents(self):
        self.applescript_helper.tell_application_process('close every document')

    def _frontmost(self):
        return wait_for(self._assert_frontmost, 10)

    def _assert_frontmost(self):
        return self.applescript_helper.get_frontmost_application() == self.name

    version = property(_get_version)
    build = property(_get_build)
    running = property(_assert_launched)
    frontmost = property(_frontmost)
