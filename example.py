from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,BooleanProperty
from kivy.garden.swipetodelete import SwipeBehavior
from kivy.lang import Builder

kvdemo='''
<DragWidget>:
    size_hint: (None,None)
    size: (625,100)
    
    swipe_rectangle: self.x, self.y , self.width, self.height
    swipe_timeout: 1000000
    swipe_distance: 1
    spacing:5

    BoxLayout:
        orientation: "horizontal"
        spacing:5
        Label:
            size_hint: .4,1
            text: "Timing :"
            font_size: 16
            canvas.before:
                Color:
                    rgba: 0.398,.310,.562,1
                Rectangle:
                    size: self.size
                    pos: self.pos
        Spinner:
            background_color: 0.398,.310,.562,1
            font_size: 16
            text: 'Select'
            values: {'08:00 AM','09:00 AM','10:00 AM','11:00 AM'}
        
        Button:
            id: btn
            text: "Ok"
            background_color: 0.398,.310,.562,1
            size_hint: .2,1

<SwipeToDeleteContainer>:
    layout_container: layout_container
    size_hint: (None, None)
    size: (675, 520)
    pos_hint: {'x':.065,'y':.065}
    do_scroll_x: False
    bar_width:'5dp'

    GridLayout:
        cols: 1
        padding: 20
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.933,.956,.956,1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint_y: None
        id: layout_container
        
        Button: 
            markup: True
            text: "[color=000000]Swipe To Delete (Click Me!)[/color]"
            font_size: 32
            size_hint: (None,None)
            size: (625,80)
            on_release: root.add_new()
                
        DragWidget:
            left_percentage: 10
            right_percentage: 10
        DragWidget:
            left_percentage: 70
            right_percentage: 70
        DragWidget:
            animation_type: 'in_bounce'
            animation_duration: 2
        DragWidget:
            remove_from_right: False
            remove_from_left: False
        DragWidget:
'''

class DragWidget(SwipeBehavior,BoxLayout):
    
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.move_to = self.x,self.y
            return super(DragWidget, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.reduce_opacity()
            return super(DragWidget, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.check_for_left()
            self.check_for_right()
            return super(DragWidget, self).on_touch_up(touch)
    
class SwipeToDeleteContainer(ScrollView):
    layout_container = ObjectProperty(None)
    '''The container which contains dragable widgets.
    :attr:`layout_container` is a :class:`~kivy.properties.ObjectProperty`,
defaults to None.
    '''
    
    def __init__(self,**kwargs):
        super(SwipeToDeleteContainer,self).__init__(**kwargs)
        self.layout_container.bind(minimum_height=self.layout_container.setter('height'))
    
    def add_new(self):
        self.ids.layout_container.add_widget(DragWidget())

class MainApp(App):
    def build(self):
        Builder.load_string(kvdemo)
        return SwipeToDeleteContainer()

if __name__ == '__main__':
    app = MainApp()
    app.run()
