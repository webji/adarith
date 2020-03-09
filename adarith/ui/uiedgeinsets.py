# Complete
"""
UIEdgeInsets with top, right, bottom and left
"""
from ..lib.utils import *
from .uiobject import UIObject


class UIEdgeInsets(UIObject):
    def __init__(self, top=0.0, right=0.0, bottom=0.0, left=0.0):
        self._top = top
        self._right = right
        self._bottom = bottom
        self._left = left
        super().__init__()

    @property
    def top(self):
        return self._top

    @property
    def right(self):
        return self._right

    @property
    def bottom(self):
        return self._bottom

    
    @property
    def left(self):
        return self._left

    @classmethod
    def to_str(cls, edge_insets: UIEdgeInsets = None):
        check_none(edge_insets)
        return f'{edge_insets.top}, {edge_insets.right}, {edge_insets.bottom}, {edge_insets.left}'


    @classmethod
    def from_str(cls, edge_insets_str: str = None):
        check_none_or_empty(edge_insets_str)
        top, right, bottom, left = edge_insets_str.strip(' ').split(',')
        return UIEdgeInsets(top, right, bottom, left)
    
    @staticmethod
    def zero():
        return UIEdgeInsets()

    def __eq__(self, value):
        if value == None or isinstance(value, UIEdgeInsets) == False:
            return False
        return self.top == value.top and self.right == value.right and self.bottom == value.bottom and self.left == value.left
        