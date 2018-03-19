import os


class Locator(object):
    """ Abstract locator class. """
    def __init__(self, locator_class):
        """
        Unfold path to the directory containing target locators.
        :param str locator_class: Locator class.
        """
        self.prefix = '%s/%s' % (os.path.dirname(__file__), locator_class)

    def __getattribute__(self, item):
        return object.__getattribute__(self, item) if item == 'prefix' \
            else '%s/%s.png' % (self.prefix, item)

    @classmethod
    def create(cls, locator_class):
        """ Create a concrete locator class. """
        return cls(locator_class)


# button = Locator.create('button')
# button2 = Locator('button')
