from kivy.clock import Clock
from kivy.properties import OptionProperty, ObjectProperty, NumericProperty, \
    ReferenceListProperty, BooleanProperty, ListProperty, AliasProperty, \
    StringProperty
from kivy.config import Config
from kivy.metrics import sp
from functools import partial
from kivy.animation import Animation

_scroll_timeout = _scroll_distance = 0
if Config:
    _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    _scroll_distance = Config.getint('widgets', 'scroll_distance')


class SwipeBehavior(object):
    '''Swipe behavior. When combined with a widget, swiping in the rectangle
    defined by :attr:`swipe_rectangle` will swipe the widget.
    In this case to left or to right.
    The example.py file demonstrates the use.
    '''

    move_to = ListProperty()
    '''To move widget.
    :attr:`remove_from_left` is a :class:`~kivy.properties.ListProperty`,
    defaults to [None,None].
    '''

    remove_from_left = BooleanProperty(True)
    '''Choice to remove the widget from the left or not.
    :attr:`remove_from_left` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to True.
    '''

    remove_from_right = BooleanProperty(True)
    '''Choice to remove the widget from the right or not.
    :attr:`remove_from_right` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to True.
    '''

    opacity_reduction_rate = NumericProperty(.005)
    '''Change the rate at which opacity reduces.
    :attr:`opacity_reduction_rate` is a :class:
    `~kivy.properties.NumericProperty`, defaults to (.005).
    '''

    animation_type = StringProperty('linear')
    '''For setting animation type.
    :attr:`animation_type` is a :class:`~kivy.properties.StringProperty`,
    defaults to linear.
    '''

    animation_duration = NumericProperty(.5)
    '''For setting animation duration.
    :attr:`animation_duration` is a :class:`~kivy.properties.NumericProperty`,
    defaults to (.5).
    '''

    right_percentage = NumericProperty(35)
    '''When to delete from right side.
    :attr:`right_percentage` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 35.
    '''

    left_percentage = NumericProperty(35)
    '''When to delete from left side.
    :attr:`left_percentage` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 35.
    '''

    swipe_distance = NumericProperty(_scroll_distance)
    '''Distance to move before swiping the :class:`swipeBehavior`, in pixels.
    As soon as the distance has been traveled, the :class:`swipeBehavior` will
    start to swipe, and no touch event will go to children.

    :attr:`swipe_distance` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 20 (pixels), according to the default value of scroll_distance
    in user configuration.
    '''

    swipe_timeout = NumericProperty(_scroll_timeout)
    '''Timeout allowed to trigger the :attr:`swipe_distance`, in milliseconds.
    If the user has not moved :attr:`swipe_distance` within the timeout,
    swiping will be disabled, and the touch event will go to the children.

    :attr:`swipe_timeout` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 55 (milliseconds), according to the default value of
    scroll_timeout in user configuration.
    '''

    swipe_rect_x = NumericProperty(0)
    '''X position of the axis aligned bounding rectangle where swiping
    is allowed. In window coordinates.

    :attr:`swipe_rect_x` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 0.
    '''

    swipe_rect_y = NumericProperty(0)
    '''Y position of the axis aligned bounding rectangle where swiping
    is allowed. In window coordinates.

    :attr:`swipe_rect_Y` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 0.
    '''

    swipe_rect_width = NumericProperty(100)
    '''Width of the axis aligned bounding rectangle where swiping is allowed.

    :attr:`swipe_rect_width` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 100.
    '''

    swipe_rect_height = NumericProperty(100)
    '''Height of the axis aligned bounding rectangle where swiping is allowed.

    :attr:`swipe_rect_height` is a :class:`~kivy.properties.NumericProperty`,
    defaults to 100.
    '''

    swipe_rectangle = ReferenceListProperty(swipe_rect_x, swipe_rect_y,
                                        swipe_rect_width, swipe_rect_height)
    '''Position and size of the axis aligned bounding rectangle where swiping
    is allowed.

    :attr:`swipe_rectangle` is a :class:`~kivy.properties.ReferenceListProperty`
    of (:attr:`swipe_rect_x`, :attr:`swipe_rect_y`, :attr:`swipe_rect_width`,
    :attr:`swipe_rect_height`) properties.
    '''

    def __init__(self, **kwargs):
        self._swipe_touch = None
        super(SwipeBehavior, self).__init__(**kwargs)

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)

    def animate_back(self):
        '''Take the widget back to its original position by using animation.
        '''
        if not self.move_to==[]:
            anim1 = Animation(x=self.move_to[0], y=self.move_to[1],
                              t=self.animation_type,
                              duration=self.animation_duration)
            anim1.start(self)
        else:
            pass

    def on_touch_down(self, touch):
        xx, yy, w, h = self.swipe_rectangle
        x, y = touch.pos

        if not self.collide_point(x, y):
            touch.ud[self._get_uid('svavoid')] = True
            return super(SwipeBehavior, self).on_touch_down(touch)
        if self._swipe_touch or ('button' in touch.profile and
                                touch.button.startswith('scroll')) or\
                not ((xx < x <= xx + w) and (yy < y <= yy + h)):
            return super(SwipeBehavior, self).on_touch_down(touch)

        # no mouse scrolling, so the user is going to swipe with this touch.
        self._swipe_touch = touch
        uid = self._get_uid()
        touch.grab(self)
        touch.ud[uid] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0}
        Clock.schedule_once(self._change_touch_mode,
                            self.swipe_timeout / 1000.)
        return True

    def on_touch_move(self, touch):
        if self._get_uid('svavoid') in touch.ud or\
                self._swipe_touch is not touch:
            return super(SwipeBehavior, self).on_touch_move(touch) or\
                self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True

        uid = self._get_uid()
        ud = touch.ud[uid]
        mode = ud['mode']
        if mode == 'unknown':
            ud['dx'] += abs(touch.dx)
            if ud['dx'] > sp(self.swipe_distance):
                mode = 'drag'
            ud['mode'] = mode
        if mode == 'drag':
            self.x += touch.dx
        return True

    def on_touch_up(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return super(SwipeBehavior, self).on_touch_up(touch)
        if self._swipe_touch and self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._swipe_touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                super(SwipeBehavior, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
        else:
            if self._swipe_touch is not touch:
                super(SwipeBehavior, self).on_touch_up(touch)
        return self._get_uid() in touch.ud

    def _do_touch_up(self, touch, *largs):
        super(SwipeBehavior, self).on_touch_up(touch)
        # don't forget about grab event!
        for x in touch.grab_list[:]:
            touch.grab_list.remove(x)
            x = x()
            if not x:
                continue
            touch.grab_current = x
            super(SwipeBehavior, self).on_touch_up(touch)
        touch.grab_current = None

    def _change_touch_mode(self, *largs):
        if not self._swipe_touch:
            return
        uid = self._get_uid()
        touch = self._swipe_touch
        ud = touch.ud[uid]
        if ud['mode'] != 'unknown':
            return
        touch.ungrab(self)
        self._swipe_touch = None
        super(SwipeBehavior, self).on_touch_down(touch)
        return

    def check_for_left(self):
        '''
        Delete the widget when on_touch_up method is called and the widget is
        left_percentage from the left.
        '''
        if hasattr(self.parent, 'width'):
            if (((self.x+self.width) - self.parent.x) / self.width
                            ) * 100 <= self.left_percentage:
                if self.remove_from_left:
                    self.parent.remove_widget(self)
            else:
                self.get_widget_back()
                self.animate_back()
        else:
            pass

    def check_for_right(self):
        '''
        Delete the widget when on_touch_up method is called and the widget is
        right_percentage from the right.
        '''
        if hasattr(self.parent, 'width'):
            if ((self.parent.width - self.x) / self.width
                        ) * 100 <= self.right_percentage:
                if self.remove_from_right:
                    self.parent.remove_widget(self)
            else:
                self.get_widget_back()
                self.animate_back()
        else:
            pass
    '''
    get the opacity of widget back
    '''
    def reduce_opacity(self):
        self.opacity -= self.opacity_reduction_rate

    def get_widget_back(self):
        self.opacity = 1.0
