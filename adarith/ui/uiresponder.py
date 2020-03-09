# Complete

class UIResponder(object):
    def __init__(self):
        self._next_responder = self
        self._prev_responder = self
        self.uikit = None
        super().__init__()

    def next(self):
        return self._next_responder

    def is_first_responder(self):
        return self._prev_responder != None and self._prev_responder != self
    
    def can_become_first_responder(self):
        return True

    # TODO, will implement later
    def become_first_responder(self):
        return False

