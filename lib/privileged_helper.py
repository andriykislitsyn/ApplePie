from os import system

from config import admin_password


class PrivilegedHelper:
    """ Privileged helper tool. Use carefully! """
    def __init__(self, password):
        self.admin_password = password

    def execute(self, command: str) -> int:
        """ Execute shell command with administrator privileges.
                :param str command: Shell script(command) to be executed.
                :return int: Return code. """
        command_: str = command.replace('"', '\\"')
        osa_cmd: str = f'do shell script "{command_}" password "{self.admin_password}" with administrator privileges'
        return system(f"osascript -e '{osa_cmd}' > /dev/null 2>&1")


privileged_helper = PrivilegedHelper(admin_password)
