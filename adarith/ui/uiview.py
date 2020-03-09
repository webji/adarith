


"""
An object that manages the content for a rectangular area on the screen.

Views are the fundamental building blocks of your app's user interface, and the UIView class defines the behaviors that are common to all views. A view object renders content within its bounds rectangle and handles any interactions with that content. The UIView class is a concrete class that you can instantiate and use to display a fixed background color. You can also subclass it to draw more sophisticated content. To display labels, images, buttons, and other interface elements commonly found in apps, use the view subclasses provided by the UIKit framework rather than trying to define your own.
Because view objects are the main way your application interacts with the user, they have a number of responsibilities. Here are just a few:

Drawing and animation
Views draw content in their rectangular area using UIKit or Core Graphics.
Some view properties can be animated to new values.

Layout and subview management
Views may contain zero or more subviews.
Views can adjust the size and position of their subviews.
Use Auto Layout to define the rules for resizing and repositioning your views in response to changes in the view hierarchy.

Event handling
A view is a subclass of UIResponder and can respond to touches and other types of events.
Views can install gesture recognizers to handle common gestures.
Views can be nested inside other views to create view hierarchies, which offer a convenient way to organize related content. Nesting a view creates a parent-child relationship between the child view being nested (known as the subview) and the parent (known as the superview). A parent view may contain any number of subviews but each subview has only one superview. By default, when a subview’s visible area extends outside of the bounds of its superview, no clipping of the subview's content occurs. Use the clipsToBounds property to change that behavior.
The geometry of each view is defined by its frame and bounds properties. The frame property defines the origin and dimensions of the view in the coordinate system of its superview. The bounds property defines the internal dimensions of the view as it sees them and is used almost exclusively in custom drawing code. The center property provides a convenient way to reposition a view without changing its frame or bounds properties directly.

https://developer.apple.com/documentation/uikit/uiview
"""


from enum import IntEnum

from ..lib.utils import *
from .uiresponder import UIResponder
from .uicolor import UIColor
from .core import CGRect, CGPoint, CGSize, CGColor

"""
The tint adjustment mode for the view.
"""
class TintAdjustmentMode(IntEnum):
    """
    The tint adjustment mode of the view is the same as its superview’s tint adjustment mode (or UIViewTintAdjustmentModeNormal if the view has no superview).
    """
    AUTOMATIC = 0

    """
    The view's tintColor property returns the completely unmodified tint color of the view.
    """
    NOTMAL = 1

    """
    The view's tintColor property returns a desaturated, dimmed version of the view's original tint color.
    """
    DIMMED = 2

class UIView(UIResponder):
    def __init__(self, frame:CGRect=CGRect(), bg_color:CGColor=CGColor.white,
        is_hidden:bool=False, alpha:float=1, is_opaque:bool=False,
        tint_color:UIColor=UIColor.label(),
        tint_adjustment_mode=TintAdjustmentMode.AUTOMATIC,
        clipse_to_bounds:bool=False, 
        clear_context_before_drawing:bool=False,
        mask:UIView=None,
        layer_class=None,
        layer = None,
        is_user_interaction_enabled:bool=False,
        bounds:CGRect=None
        ):
        self.frame = frame
        self.bg_color = bg_color
        self.is_hidden = is_hidden
        self.alpha = alpha
        self.is_opaque = is_opaque
        self.tint_color = tint_color
        self.tint_adjustment_mode = tint_adjustment_mode
        self.clips_to_bounds = clipse_to_bounds
        self.clear_context_before_drawing = clear_context_before_drawing
        self.mask = mask
        self.layer_class = layer_class
        self.layer = layer
        self.is_user_interaction_enabled = is_user_interaction_enabled

        if bounds == None:
            self.bounds = CGRect(CGPoint, frame.size)

        self.superview = None
        self.subviews = []
        super().__init__()

    
    def on(self, frame:CGRect=CGRect(), bg_color:CGColor=CGColor.white,
        is_hidden:bool=False, alpha:float=1, is_opaque:bool=False,
        tint_color:UIColor=UIColor.label(),
        tint_adjustment_mode=TintAdjustmentMode.AUTOMATIC,
        clipse_to_bounds:bool=False, 
        clear_context_before_drawing:bool=False,
        mask:UIView=None,
        layer_class=None,
        layer = None,
        is_user_interaction_enabled:bool=False
        ):
        pass


    @property
    def center(self):
        return CGPoint(self.frame.x + self.frame.w/2, self.frame.y + self.frame.h/2)

    
    # TODO: Animated to transform based on duration
    def transform(self):
        pass


    def index_of_subview(self, view:UIView=None):
        check_none(view)
        index = None
        try:
            index = self.subviews.index(view)
        except ValueError as e:
            index = None


    def add_subview(self, view:UIView=None):
        check_none(view)
        self.subviews.append(view)

    
    def remove_subView(self, view:UIView=None):
        check_none(view)
        if view not in self.subviews:
            raise ArgumentError('The view does not in the subview list')
        self.subviews.remove(view)


    def bring_subview_to_front(self, view:UIView=None):
        check_none(view)
        if view not in self.subviews:
            raise ArgumentError('The view does not in the subview list')
        
        self.subviews.remove(view)
        self.subviews.append(view)


    def send_subview_to_back(self, view:UIView=None):
        check_none(view)
        if view not in self.subviews:
            raise ArgumentError('The view does not in the subview list')
        
        self.subviews.remove(view)
        self.subviews.insert(0, view)


    def remove_from_superview(self):
        self.superview.remove(self)
        self.superview = None

    
    def insert_subview(self, view:UIView=None, atIndex:int=0):
        check_none(view)
        check_none(atIndex)
        index = min(atIndex, len(self.subviews))
        self.subviews.insert(index, view)

    
    def insert_subview_before(self, view:UIView=None, target:UIView=None):
        check_none(view)
        check_none(target)
        index = self.index_of_subview(target)
        if index == None:
            raise ArgumentError('target view is not a subview')
        else:
            self.insert_subview(view, index)

    
    def exchange_subview(self, v1_index:int=None, v2_index:int=None):
        check_none(v1_index)
        check_none(v2_index)
        max_index = max(v1_index, v2_index)
        if max_index > len(self.subviews):
            raise ArgumentError(f'index {max(v1_index, v2_index)} is out of scope {len(self.subviews)}')
        
        min_index = min(v1_index, v2_index)
        # The below 4 process should in the exact order
        # pop the max view
        max_view = self.subviews.pop(max_index)
        # pop the min view
        min_view = self.subviews.pop(min_index)
        # insert the min view
        self.subviews.insert(min_index, max_view)
        # insert the max view
        self.subviews.insert(max_index, min_view)

    
    def is_descendant_of(self, view:UIView=None):
        check_none(view)
        test_view = self 
        # check through all the ancestors
        while test_view.superview:
            if test_view.superview == view:
                return True
            test_view = test_view.superview
        return False


