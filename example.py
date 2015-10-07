''' Import Statements '''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,BooleanProperty
from SwipeToDeleteBehavior import SwipeBehavior
from kivy.animation import Animation
from kivy.lang import Builder
from time import sleep

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
        
        Label: 
            markup: True
            text: "[color=000000]Swipe To Delete[/color]"
            font_size: 32
            size_hint: (None,None)
            size: (625,80)
                
        DragWidget:
        DragWidget:
        DragWidget:
        DragWidget:
        DragWidget: 
        DragWidget:
'''

class DragWidget(SwipeBehavior,BoxLayout):
    
    widget_original_cord = ListProperty([0,0])
    ''' To remember the original coordinates of the widget.
    :attr:`widget_original_cord` is a :class:`~kivy.properties.ListProperty`,
defaults to [0,0].
    '''
    bool = BooleanProperty(True)
    '''To prevent manipulation of original coordinates of the widget.
    :attr:`bool` is a :class:`~kivy.properties.BooleanProperty`,
defaults to True.
    '''
    
    def AnimateBack(self):
        '''Take the widget back to its original position by using animation.
        '''
        anim1 = Animation(x=self.widget_original_cord[0],y=self.widget_original_cord[1], t='linear',duration = .5)
        anim1.start(self)
    
    def RemoveWidget(self,instance):
        '''Remove the widget
        '''
        instance.parent.remove_widget(instance)
        
    def CheckForLeft(self):
        '''Delete the widget when on_touch_up method is called and the widget is 25% or less left inside, from the left.
        '''
        if (((self.x+self.width) - self.parent.x )/self.width)*100 <= 35:
            self.RemoveWidget(self)
        else:
            self.AnimateBack()
    
    def CheckForRight(self):
        '''Delete the widget when on_touch_up method is called and the widget is 25% or less left inside, from the right.
        '''
        if ((self.parent.width - self.x)/self.width)*100 <= 35:
            self.RemoveWidget(self)
        else:
            self.AnimateBack()
            
    
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            try:
                if self.bool:
                    self.widget_original_cord = [self.x,self.y]
                    self.bool = False
                return super(DragWidget, self).on_touch_down(touch)
            except:
                pass
    
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            try:
                if self.bool:
                    self.widget_original_cord = [self.x,self.y]
                    self.bool = False
                return super(DragWidget, self).on_touch_move(touch)
            except:
                pass

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            try:
                self.CheckForRight()
                self.CheckForLeft()
                return super(DragWidget, self).on_touch_up(touch)
            except:
                pass
        

class SwipeToDeleteContainer(ScrollView):
    layout_container = ObjectProperty(None)
    '''The container which contains dragable widgets.
    :attr:`layout_container` is a :class:`~kivy.properties.ObjectProperty`,
defaults to None.
    
    '''
    
    def __init__(self,**kwargs):
        super(SwipeToDeleteContainer,self).__init__(**kwargs)
        self.layout_container.bind(minimum_height=self.layout_container.setter('height'))

class MainApp(App):
    def build(self):
        Builder.load_string(kvdemo)
        return SwipeToDeleteContainer()

if __name__ == '__main__':
    app = MainApp()
    app.run()