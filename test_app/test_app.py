from lib.application import Application


class TestApp(Application):
    def __init__(self):
        super(TestApp, self).__init__('TestApp')


test_app = TestApp()
