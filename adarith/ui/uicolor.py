"""

The standard color objects you can use for labels, text, backgrounds, links, and more.

UI Element Colors
UIKit provides standard color objects for the foreground and background colors of your app's UI elements. The names of these color objects reflect their intended use, rather than specific color values.
Except where noted, standard color objects adapt automatically to Dark Mode changes when you use the provided UIColor object. If you retrieve the color values, either directly or using another type such as CGColor, you must handle Dark Mode changes yourself. For more information about supporting Dark Mode, see Supporting Dark Mode in Your Interface.
https://developer.apple.com/documentation/uikit/uicolor/ui_element_colors


Standard Colors
The standard color objects for specific shades, such as red, blue, green, black, white, and more.
Overview
Use the standard color objects when you want to use a specific color shade in your UI.
The system color objects adapt automatically to Dark Mode changes when you use the provided UIColor object, but the fixed-shade colors don't adapt. If you retrieve the color values, either directly or using another type such as CGColor, you must handle Dark Mode changes yourself. For more information about supporting Dark Mode, see Supporting Dark Mode in Your Interface.
https://developer.apple.com/documentation/uikit/uicolor/standard_colors
"""



from .uiobject import UIObject

from .core import CGColor
from .uiimage import UIImage

class UIColor(UIObject):
    def __init__(self, gray:float=0.5, r:float=0, g:float=0, b:float=0, alpha:float=1,
        pattern_image:UIImage=UIImage()):
        self.cgcolor = CGColor(gray, r, g, b, alpha)
        self.pattern_image = pattern_image
        super().__init__()



    def on(self, cgcolor:CGColor=None, pattern_image:UIImage=None):
        if cgcolor != None:
            self.cgcolor = cgcolor
        if pattern_image != None:
            self.pattern_image = pattern_image
        return self



    """
    The color for text labels that contain primary content.
    """
    @classmethod
    def label(cls):
        return UIColor().on(cgcolor=CGColor.gray_9())

    """
    The color for text labels that contain secondary content.
    """
    @classmethod
    def secondary_label(cls):
        return UIColor().on(cgcolor=CGColor.gray_8())


    """
    The color for text labels that contain tertiary content.
    """    
    @classmethod
    def tertiary_label(cls):
        return UIColor().on(cgcolor=CGColor.gray_7())
    
    """
    The color for text labels that contain quaternary content.
    """
    @classmethod
    def quaternary_label(cls):
        return UIColor().on(cgcolor=CGColor.gray_6())
