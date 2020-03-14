


def Singleton(cls):
    _instance = {}

    def _inner():
        if cls not in _instance:
            _instance[cls]  = cls()
        return _instance[cls]

    return _inner()

