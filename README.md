Swipe To Delete
=============

![ScreenShot](https://raw.github.com/kiok46/swipetodelete/master/screenshot.png)

##Usage Summary

This project is an implementation of Swipe Behavior. 
SwipeToDelete widget is built on Swipe Behaviour as a test case.
This widget can be used to create dynamic layouts where users can delete UI widgets by swiping them left or right. 
Swipe behavior, when combined with a widget allows swiping within a rectangular area.

Latest commit adds some new features.

##How It Works


Import in your python file or kivy file
```
from kivy.garden.swipetodelete import SwipeBehavior
class DragWidget(SwipeBehavior,BoxLayout):
```
Use in your kivy file or python file
```
<DragWidget>:
  swipe_rectangle: self.x, self.y , self.width, self.height
  swipe_timeout: 1000000
  swipe_distance: 1
```

See example.py file for more.

##SwipeBehaviour Properties

- *swipe_distance* - Distance to move before swiping. NumericProperty(20)
- *swipe_timeout* - Timeout allowed to trigger swipe_distance in milliseconds. NumericProperty(55)
- *swipe_rect_x* - X position of the axis aligned bounding rectangle where swiping
    is allowed. NumericProperty(0)
- *swipe_rect_y* - Y position of the axis aligned bounding rectangle where swiping
    is allowed. NumericProperty(0)
- *swipe_rect_width* - Width of the axis aligned bounding rectangle where swiping is allowed. NumericProperty(100)
- *swipe_rect_height* - Height of the axis aligned bounding rectangle where swiping is allowed. NumericProperty(100)
- *swipe_rectangle* - Position and size of the axis aligned bounding rectangle where swiping
    is allowed. ReferenceListProperty(swipe_rect_x, swipe_rect_y, swipe_rect_width, swipe_rect_height) 
- *remove_from_left* - User has the choice to remove the widget from the left or not.
- *remove_from_right* - User has the choice to remove the widget from the right or not.
- *animation_type* - For different animation while returning back.
- *animation_duration* - Duration of animation
- *right_percentage* - Decide the limit to delete when user swipes to the right side.
- *left_percentage* - Decide the limit to delete when user swipes to left side.
- *move_to* - To move widgets
- *opacity_reduction_rate* - Change the way at which opacity reduces.


##Want to contribute or need to see some improvements?
I would love that, please create an issue or send a PR.








