import math

from .sign import SignType
from .scale import ScaleType

class Number(object):

    def __init__(self, scale=ScaleType(), sign=SignType(), absValue=0.0, radix=0):
        self.scale = scale
        self.sign = sign
        self.absValue = absValue
        self.radix = radix
        super().__init__()

    def __repr__(self):
        sign = ''
        if self.sign.type == SignType.NEGATIVE:
            sign = '-'
        
        value = 'NA'
        if self.radix == 0:
            value = f'{int(self.absValue)}' 
        else:
            value = f'{self.absValue}'

        return f'{sign}{value}'

    @property
    def decValue(self):
        return self.sign.type * int(self.absValue)

    @property
    def floatValue(self):
        return self.sign.type * self.absValue

    @staticmethod
    def of(value = 0, sign=SignType):
        radix = 0
        if type(value) == float:
            redix = 2
        
        sign = SignType.of(value=value)
        
        return Number(scale=ScaleType.DEC, sign=sign, absValue=math.fabs(value), radix=radix)