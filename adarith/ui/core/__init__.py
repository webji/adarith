from enum import IntEnum

from ...lib.utils import *



class CGPoint:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        super().__init__()

    def to_tuple(self):
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, x, y):
        return CGPoint(x, y)

    def to_str(self):
        return f'{self.x}, {self.y}'

    @classmethod
    def from_str(cls, point:str=None):
        x, y = point.strip(' ').split(',')
        return CGPoint(x, y)

class CGSize:
    def __init__(self, w=0.0, h=0.0):
        self.w = w
        self.h = h
        super().__init__()

    def to_tuple(self):
        return (self.w, self.h)

    @classmethod
    def from_tuple(cls, w, h):
        return CGSize(w, h)

    def to_str(self):
        return f'{self.w}, {self.h}'

    @classmethod
    def from_str(cls, size:str=None):
        x, y = size.strip(' ').split(',')
        return CGSize(w, h)


class CGRect:
    def __init__(self, x:float=0.0, y:float=0.0, w:float=0.0, h:float=0.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super().__init__()

    def to_tuple(self):
        return (self.x, self.y, self.w, self.h)

    @classmethod
    def from_tuple(cls, x, y, w, h):
        return CGRect(x, y, w, h)

    def to_str(self):
        return f'{self.x}, {self.y}, {self.w}, {self.h}'

    @classmethod
    def from_str(cls, rect:str=None):
        check_none_or_empty(rect)
        x, y, w, h = rect.strip(' ').split(',')
        return CGRect(x, y, w, h)

    @property
    def point(self):
        return CGPoint(self.x, self.y)
    
    @property
    def size(self):
        return CGSize(self.w, self.h)

    @property
    def center(self):
        return CGPoint((self.x + self.w) >> 1, (self.y + self.h) >> 1)

    def set_x_y(self, x:float=0.0, y:float=0.0):
        self.x = x
        self.y = y

    def set_point(self, point:CGPoint=CGPoint()):
        check_none(point)
        self.x = point.x
        self.y = point.y
       

    def set_w_h(self, w:float=0.0, h:float=0.0):
        self.w = w
        self.h = h

    def set_size(self, size:CGSize=CGSize()):
        check_none(size)
        self.w = size.w
        self.h = size.h

    

class CGColor:
    def __init__(self, gray:float=1, r:float=0.0, g:float=0.0, b:float=0.0, alpha:float=1):
        self.gray = gray
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha
        super().__init__()

    def on(self, gray:float=None, r:float=None, g:float=None, b:float=None, alpha:float=None):
        if gray != None:
            self.gray = gray
        if r != None:
            self.r = r
        if g != None:
            self.g = g
        if b != None:
            self.b = b
        if alpha != None:
            self.alpha = alpha
        return self

    @classmethod
    def black(cls):
        return CGColor()

    @classmethod
    def white(cls):
        return CGColor(r=255, g=255, b=255)
    
    @classmethod
    def clear(cls):
        return CGColor()

    
    @classmethod
    def red(cls):
        return CGColor(r=255)

    @classmethod
    def green(cls):
        return CGColor(g=255)

    @classmethod
    def blue(cls):
        return CGColor(b=255)


    @classmethod
    def yellow(cls):
        return CGColor(r=255, g=255)

    @classmethod
    def gray_9(cls):
        return CGColor.white().on(gray=0.1)
    
    @classmethod
    def gray_8(cls):
        return CGColor.white().on(gray=0.2)

    @classmethod
    def gray_7(cls):
        return CGColor.white().on(gray=0.3)

    @classmethod
    def gray_6(cls):
        return CGColor.white().on(gray=0.4)

    @classmethod
    def gray_5(cls):
        return CGColor.white().on(gray=0.5)

    @classmethod
    def gray_4(cls):
        return CGColor.white().on(gray=0.6)

    @classmethod
    def gray_3(cls):
        return CGColor.white().on(gray=0.7)

    @classmethod
    def gray_2(cls):
        return CGColor.white().on(gray=0.8)

    @classmethod
    def gray_1(cls):
        return CGColor.white().on(gray=0.9)


"""
These blend mode constants represent the Porter-Duff blend modes. The symbols in the equations for these blend modes are:
R is the premultiplied result
S is the source color, and includes alpha
D is the destination color, and includes alpha
Ra, Sa, and Da are the alpha components of R, S, and D
You can find more information on blend modes, including examples of images produced using them, and many mathematical descriptions of the modes, in PDF Reference, Fourth Edition, Version 1.5, Adobe Systems, Inc. If you are a former QuickDraw developer, it may be helpful for you to think of blend modes as an alternative to transfer modes
For examples of using blend modes see "Setting Blend Modes" and "Using Blend Modes With Images" in Quartz 2D Programming Guide.
https://developer.apple.com/documentation/coregraphics/cgblendmode
"""
class CGBlendMode(IntEnum):
    """
    Paints the source image samples over the background image samples.
    """
    NORMAL = 0

    """
    Multiplies the source image samples with the background image samples. This results in colors that are at least as dark as either of the two contributing sample colors.
    """
    MULTIPY = 1
    
    """
    Multiplies the inverse of the source image samples with the inverse of the background image samples, resulting in colors that are at least as light as either of the two contributing sample colors.
    """
    SCREEN = 2

    OVERLAY = 3

    DARKEN = 4

    LIGHTEN = 5

    """
    Brightens the background image samples to reflect the source image samples. Source image sample values that specify black do not produce a change.
    """
    COLORDODGE = 6

    """
    Darkens the background image samples to reflect the source image samples. Source image sample values that specify white do not produce a change.
    """
    COLORBRUN = 7

    SOFTLIGHT = 8

    HARDLIGHT = 9

    DIFFERENCE = 10

    """
    Produces an effect similar to that produced by 
CGBlendMode.difference
, but with lower contrast. Source image sample values that are black don’t produce a change; white inverts the background color values.
    """
    EXCLUSION = 11

    """
    Uses the luminance and saturation values of the background with the hue of the source image.
    """
    HUE = 12

    """
    Uses the luminance and hue values of the background with the saturation of the source image. Areas of the background that have no saturation (that is, pure gray areas) don’t produce a change.
    """
    SATURATION = 13

    """
    Uses the luminance values of the background with the hue and saturation values of the source image. This mode preserves the gray levels in the image. You can use this mode to color monochrome images or to tint color images.
    """
    CLOLR = 14

    """
    Uses the hue and saturation of the background with the luminance of the source image. This mode creates an effect that is inverse to the effect created by 
CGBlendMode.color
.
    """
    LUMINOSITY = 15

    """
    R = 0
    """
    CLEAR = 16

    """
    R = S
    """
    COPY = 17

    """
    R = S * Da
    """
    SOURCEIN = 18

    """
    R = S * (1 - Da)
    """
    SOURCEOUT = 19

    """
    R = S*Da + D*(1-Sa)
    """
    SOURCEATOP = 20

    """
    R = S*(1-Da) + D
    """
    DESTINATIONOVER = 21

    """
    R = D*Sa
    """
    DESTINATIONIN = 22

    """
    R = D*(1-Sa)
    """
    DEATINATIONOUT = 23

    """
    R = S*(1 - Da) + D*Sa
    """
    DEATINATIONATOP = 24

    """
    R = S*(1 - Da) + D*(1 - Sa). This XOR mode is only nominally related to the classical bitmap XOR operation, which is not supported by Core Graphics
    """
    XOR = 25

    """
    R = MAX(0, 1 - ((1 - D) + (1 - S)))
    """
    PLUSDARKER = 26

    """
    R = MIN(1, S + D)
    """
    PLUSLIGHTER = 27

