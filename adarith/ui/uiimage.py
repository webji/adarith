# InComplete
"""
An object that manages image data
https://developer.apple.com/documentation/uikit/uiimage

You use image objects to represent image data of all kinds, and the UIImage class is capable of managing data for all image formats supported by the underlying platform. Image objects are immutable, so you always create them from existing image data, such as an image file on disk or programmatically created image data. An image object may contain a single image or a sequence of images you intend to use in an animation.
You can use image objects in several different ways:
Assign an image to a UIImageView object to display the image in your interface.
Use an image to customize system controls such as buttons, sliders, and segmented controls.
Draw an image directly into a view or other graphics context.
Pass an image to other APIs that might require image data.
Although image objects support all platform-native image formats, it is recommended that you use PNG or JPEG files for most images in your app. Image objects are optimized for reading and displaying both formats, and those formats offer better performance than most other image formats. Because the PNG format is lossless, it is especially recommended for the images you use in your app’s interface.
"""
from enum import IntEnum

from .uiobject import UIObject
from .uiedgeinsets import UIEdgeInsets

from ..lib.image import Image
from ..lib.utils import *

from .core import CGPoint, CGSize, CGRect, CGBlendMode

class ImageOrientations(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_MIRRORED = 4
    DOWN_MIRRORED = 5
    LEFT_MIRRORED = 6
    RIGHT_MIRRORED = 7


class ImageResizingMode(IntEnum):
    TILE = 0
    STRETCH = 1


class ImageRenderingMode(IntEnum):
    """
    Use the default rendering mode for the context where the image is used.
    """
    AUTOMATIC = 0

    """
    Always draw the original image, without treating it as a template.
    """
    ALWAYSORIGINAL = 1

    """
    Always draw the image as a template image, ignoring its color information.
    """
    ALWAYSTEMPLATE = 2

class UIImage(UIObject):
    def __init__(self):
        self._image = None
        self._image_list = []
        self._image_orientation = ImageOrientations.UP
        self._flips_for_right_to_left_layout_direction = False
        self._resizing_mode = ImageResizingMode.TILE
        self._duration = 0
        self._capInsets = UIEdgeInsets()
        self._alignmentRectInsets = UIEdgeInsets()
        self._rendering_mode = ImageRenderingMode.AUTOMATIC
        self._scale = 1
        self._size = CGSize()
        super().__init__()

    """
    Determines how an image is rendered.
    Default: AUTOMATIC
    """
    @property
    def rendering_mode(self):
        return self._reendering_mode


    def init_with_path(self, path: str = None):
        check_none_or_empty(lists=path)
        self._image = Image(path).image
        self._image_list.append(self._image)

    def init_with_image(self, image=None):
        check_none(target=image)
        if self._image == None:
            self._image = image
            self._image_list = []
            self._image_list.append(self._image)

    def add(self, image=None):
        if self._imsage == None:
            self.init_with_image(image=image)
        else:
            self._image_list.append(image)

    
    def remove(self, image=None):
        check_none(target=image)
        if self._image == image:
            self._image_list.remove(image)
            self._image = None
            if len(self._image_list) > 0:
                self._image = self._image_list.pop()
        else:
            self._image_list.remove(image)
    

    def on(self, image_orientation=None, 
        flips_for_right_to_left_layout_direction=None, 
        resizing_mode=None, duration=None, capInsets=None,
        alignmentRectInsets=None, rendering_mode=None,
        scale=None, size=None ):
        if image_orientation != None:
            self._image_orientation = image_orientation
        if flips_for_right_to_left_layout_direction != None:
            self._flips_for_right_to_left_layout_direction = flips_for_right_to_left_layout_direction
        if resizing_mode != None:
            self._resizing_mode = resizing_mode
        if duration != None:
            self._duration = duration
        if capInsets != None:
            self._capInsets = capInsets
        if alignmentRectInsets != None:
            self._alignmentRectInsets = alignmentRectInsets
        if rendering_mode != None:
            self._rendering_mode = rendering_mode
        if scale != None:
            self._scale = scale
        if size != None:
            self._size = size
        return self
    
    def draw_at(self, point:CGPoint=CGPoint(), blendMode:CGBlendMode=CGBlendMode.NORMAL, alpha:float=1):
        check_none(point)
        # TODO Draw the image at Point

    
    def draw_in(self, rect:CGRect=CGRect(), blendMode:CGBlendMode=CGBlendMode.NORMAL, alpha:float=1):
        check_none(rect)
        # TODO Draw the image at Point

    