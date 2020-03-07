class OperationType(object):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 4

    def __init__(self, type=ADD):
        self.type = type
        super().__init__()

    def __repr__(self):
        if self.type == OperationType.ADD:
            return '+'
        elif self.type == OperationType.SUB:
            return '-'
        elif self.type == OperationType.MUL:
            return '*'
        elif self.type == OperationType.DIV:
            return '/'
        else:
            return 'NA'