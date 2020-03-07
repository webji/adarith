class ScaleType(object):
    BIN = 2
    OCT = 8
    DEC = 10
    HEX = 16

    def __init__(self, type=DEC):
        self.type = type
        super().__init__()

    def __repr__(self):
        if self.type == ScaleType.BIN:
            return 'BIN-2'
        elif self.type == ScaleType.OCT:
            return 'OCT-8'
        elif self.type == ScaleType.DEC:
            return 'DEC-10'
        elif self.type == ScaleType.HEX:
            return 'HEX-16'
        else:
            return 'NA'
            