import threading


class EnvDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.Lock()

    def __setitem__(self, key, value):
        with self.lock:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        with self.lock:
            super().__delitem__(key)

    def __getitem__(self, key):
        with self.lock:
            return super().__getitem__(key)

    def __contains__(self, item):
        with self.lock:
            return super().__contains__(item)

    def items(self):
        with self.lock:
            return super().items()

    def values(self):
        with self.lock:
            return super().values()

    def pop(self, key, default=None):
        with self.lock:
            return super().pop(key, default)

    def popitem(self):
        with self.lock:
            return super().popitem()

    def clear(self):
        with self.lock:
            return super().clear()

    def update(self, *args, **kwargs):
        with self.lock:
            return super().update(*args, **kwargs)

    def setdefault(self, key, default=None):
        with self.lock:
            return super().setdefault(key, default)
