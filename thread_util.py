import threading

class Flag(threading.Event):
    """A wrapper for the typical event class to allow for overriding the
    `__bool__` magic method, since it looks nicer.
    """
    def __bool__(self):
        return self.is_set()
