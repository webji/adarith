

class SignType(object):
    POSITIVE = 1
    NEGATIVE = -1

    def __init__(self, type=POSITIVE):
        self.type = type
        super().__init__()
    
    @staticmethod
    def of(value = 0):
        if value >= 0.0:
            return SignType(type=SignType.POSITIVE)
        else:
            return SignType(type=SignType.NEGATIVE)