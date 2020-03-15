


def Singleton(cls):
    _instance = {}

    def _inner(*args, **kwargs):
        if cls not in _instance:
            _instance[cls]  = cls(*args, **kwargs)
        return _instance[cls]

    return _inner

