import applescript


class AppleScriptHelper:
    """ AppleScript wrapper that works with a dedicated process/application process. """
    def __init__(self, process):
        self.process = process

    def click(self, element):
        return self.perform_action(element, 'AXPress')

    def perform_action(self, element, action):
        return self._execute(self.tell_application_process('perform action "{0}" of {1}'.format(action, element)))

    def assert_element_exists(self, element):
        return self._execute(self.tell_application_process('return exists {0}'.format(element)))

    def get_element_name(self, element):
        return self.get_element_property(element, 'name')

    def get_element_title(self, element):
        return self.get_element_attribute(element, 'AXTitle')

    def get_element_size(self, element):
        return self.get_element_attribute(element, 'AXSize')

    def get_element_position(self, element):
        return self.get_element_attribute(element, 'AXPosition')

    def assert_element_enabled(self, element):
        return self.get_element_attribute(element, 'AXEnabled')

    def assert_element_focused(self, element):
        return self.get_element_attribute(element, 'AXFocused')

    def get_element_attribute(self, element, attribute):
        return self.get_element_property(element, 'value of attribute "{0}"'.format(attribute))

    def get_element_property(self, element, property_):
        return self._execute(self.tell_application_process('return {0} of {1}'.format(property_, element)))

    def get_frontmost_application(self):
        get_frontmost_process = 'return name of the first process whose frontmost is true'
        return self._execute(self.tell_system_events(get_frontmost_process))

    def get_processes_list(self):
        return self._execute(self.tell_system_events('return name of every process'))

    def tell_application_process(self, command):
        return self.tell_system_events('tell application process "{0}" to {1}'.format(self.process, command))

    def keystroke(self, text):
        self._execute(self.tell_system_events('keystroke "{0}"'.format(text)))

    def press_key(self, key_code):
        self._execute(self.tell_system_events('key code {0}'.format(key_code)))

    def tell_application(self, command):
        return self._execute('tell application "{0}" to {1}'.format(self.process, command))

    @staticmethod
    def tell_system_events(command):
        return 'tell application "System Events" to {0}'.format(command)

    @staticmethod
    def _execute(command):
        return applescript.AppleScript(source=str(command)).run()
