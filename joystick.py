from math import hypot
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import threading, time
from kivy.clock import Clock

class Joystick(Widget):
    BG ={
        'Color': (.5,.5,.5,1),
        'Size': 2*(dp(100),),
        'Variation': (0,0)
    }

    JS ={
        'Color': (.8,.8,.8,1),
        'Size': 2*(dp(80),),
        'Variation': (0,0)
    }


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isDown = False
        self.previous = {}
        self.lastTouch: tuple[float, float] = (0,0)

        Clock.schedule_once(self.draw, 1/30)
        threading.Thread(target = self.recenter, args = (self,)).start()
        threading.Thread(target = self.on_change, args= ('self.JS["Variation"]', self.on_js_change)).start()

    def draw (self, *args):
        self.center = [
            self.pos[i] + self.size[i]/2 for i in range(len(self.pos))
        ]
        self.canvas.clear()
        with self.canvas:
            for part in (self.BG, self.JS):
                Color(rgb = part['Color'])
                RoundedRectangle(
                    pos = [self.center[i] - part['Size'][i]/2 + part['Variation'][i] for i, _ in enumerate(self.center)],
                    size = part['Size'],
                    radius = 2*[size/2 for size in part['Size']]
                )
        Clock.schedule_once(self.draw, 1/30)
    
    def on_touch_down(self, touch):
        if (not self.isDown) and hypot(touch.x - self.center[0] + self.JS['Variation'][0], touch.y - self.center[1] + self.JS['Variation'][1]) < self.BG['Size'][0]:
            self.isDown = True
            self.lastTouch = (touch.x, touch.y)

    def on_touch_move(self, touch):
        if not self.isDown:
            return super().on_touch_move(touch)
        
        if self.lastTouch == None:
            return super().on_touch_move(touch)

        if hypot(touch.x-self.lastTouch[0], touch.y - self.lastTouch[1]) > dp(200):
            return super().on_touch_move(touch)
        
        self.lastTouch = touch.x, touch.y
        
        dx, dy = touch.x - self.center[0], touch.y - self.center[1]

        if hypot(dx, dy) >= self.JS['Size'][0]/2:
            factor = self.JS['Size'][0]/ 2 / hypot(dx,dy)
            dx, dy = [d*factor for d in (dx,dy)]
        
        self.JS['Variation'] = dx, dy
        self.draw()
        return super().on_touch_move(touch)
        
    def on_touch_up(self, touch):
        if hypot(touch.x - self.lastTouch[0], touch.y - self.lastTouch[1]) <= dp(200):
            self.isDown = False

        return super().on_touch_up(touch)

    def recenter(self, *args):
        if self:
            if not self.isDown:
                self.JS['Variation'] = [
                    variation // 2 for variation in self.JS['Variation']
                ]
                self.lastTouch = [self.center[i] + self.JS['Variation'][i] for i in range(2)]
            threading.Thread(target = self.recenter, args = (self,)).start()
    
    def on_change(self, property_name, function):
        exec(''.join(f'''
            current_value, previous = {property_name}, self.previous.get(property_name, None)
            if current_value != self.previous.get(property_name, None):
                self.previous[property_name] = current_value
                function(current_value, previous)
            threading.Thread(target=self.on_change, args = (property_name, function)).start()
        '''.split('            ')))
    
    @staticmethod
    def on_js_change(self, current, previous):
        ...

    @property
    def directions(self):
        return [variation/(self.JS['Size'][i]/2) for i, variation in enumerate(self.JS['Variation'])]
