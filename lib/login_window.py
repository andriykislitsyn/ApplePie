import os

import Quartz

from lib.applescript_helper import AppleScriptHelper
from config import admin_password


class LoginWindow:
    def __init__(self):
        self.applescript_helper = AppleScriptHelper('loginwindow')

    def unlock_screen(self):
        if not self.screen_locked:
            return
        self.wake_up()
        self.applescript_helper.press_key(117)
        self.applescript_helper.keystroke(admin_password)
        self._confirm_login()

    def assert_screen_locked(self):
        cgsession = dict(Quartz.CGSessionCopyCurrentDictionary())
        return cgsession.get('CGSSessionScreenIsLocked') is not None

    screen_locked = property(assert_screen_locked)

    def _confirm_login(self):
        self.applescript_helper.click(element='button 1 of window "Login Panel"')

    def wake_up(self):
        self.applescript_helper.press_key(123)
        os.system('sleep 2; caffeinate -u -t 2')

    @staticmethod
    def start_screen_saver():
        os.system('open -a ScreenSaverEngine')
