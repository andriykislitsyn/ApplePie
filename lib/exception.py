
class LocatorResourceMissing(Exception):
    """ Locator resource (screenshot) not found in target directory. """
    pass


class PatternNotFound(Exception):
    """ Pattern not found on screen. """
    pass
