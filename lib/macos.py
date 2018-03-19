from subprocess import check_output
from datetime import datetime
from os import system, path, walk
import random
import re
import string


class MacOS:
    @staticmethod
    def generate_random_password(password_length):
        symbols = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(symbols) for _ in range(password_length))

    @staticmethod
    def show_document(document):
        system('open -R "%s"' % document)

    @staticmethod
    def take_screenshot(destination, scr_name):
        system('screencapture -x "%s"' % (path.join(destination, scr_name)))
        return path.join(destination, scr_name)

    @staticmethod
    def clear_folder(folder):
        system('rm -rf "%s"/*' % folder)

    @staticmethod
    def remove_folder(folder):
        system('rm -rf "%s"' % folder)

    @staticmethod
    def count_directory_files(target_directory):
        files_count = check_output('cd "%s"; ls -F |grep -v / | wc -l' % target_directory, shell=True).strip()
        if 'No such file or directory' in files_count:
            return 0
        return int(files_count)

    @staticmethod
    def count_directory_items(directory, file_name, extension, case):
        files_count = 0
        for cats, dirs_, files in walk(directory):
            for file_ in files:
                if case == 'all':
                    if file_.endswith(extension) and file_name in file_:
                        files_count += 1
                elif case == 'any':
                    if file_.endswith(extension) or file_name in file_:
                        files_count += 1
        return files_count

    @staticmethod
    def convert_to_bytes(size_string):
        multipliers = {'bytes': 10 ** 0, 'KB': 10 ** 3, 'MB': 10 ** 6, 'GB': 10 ** 9}
        size = float(re.search('\d+\.\d+|\d+', size_string).group())
        literal = re.search('\wB|bytes', size_string).group()
        return int(size * multipliers[literal])

    def get_mac_model(self):
        return str(check_output(['sysctl', 'hw.model'])).split(':')[-1].strip()

    def get_serial_number(self):
        return check_output("system_profiler SPHardwareDataType |awk '/Serial/ {print $4}'", shell=True)

    def generate_date_stamp(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    mac_model = property(get_mac_model)
    serial_number = property(get_serial_number)
    timestamp = property(generate_date_stamp)


macos = MacOS()
