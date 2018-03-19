from time import sleep, time


def wait_for(predicate, wait=20, *args, **kwargs):
    """
    Attempts to call a function/method and exits on successful attempt
    :param predicate: a function or method to be executed
    :param wait: wait time
    :param args: predicate arguments
    :param kwargs: predicate key arguments
    :return bool: True on success or False on time out
    """
    end = time() + wait
    while time() < end:
        result = predicate(*args, **kwargs)
        if result:
            return True
        sleep(0.5)
    return False
