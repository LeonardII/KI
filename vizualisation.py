import pyglet
from pyglet import shapes
from enum import Enum
from algo import Point, Params
from pyglet.window import mouse
from pyglet.text import Label


class UIStatus(Enum):
    STARTWAHL = 0
    ZIELWAHL = 1
    STARTBERECHNUNG = 2

class Vizu(pyglet.window.Window):
    def __init__(self, board, parameters: Params):
        self.parameter_input_width = 200
        super().__init__(width=1000 + self.parameter_input_width, height=1000)
        self.parameters = parameters
        self.batch = pyglet.graphics.Batch()
        self.b = []

        lange_seite = max(len(board),len(board[0]))
        self.rect_width = self.height/lange_seite
        i = 0
        for row in board:
            for cell in row:
                number = int(cell)
                self.b.append(shapes.Rectangle(*self.coord_to_window((i%40), int(i/40), False),self.rect_width, self.rect_width, color=self.get_color(number), batch=self.batch))
                i+=1
        
        self.startPoint = Point(0,0)
        self.startTile = None
        self.goalPoint = Point(0,0)
        self.goalTile = None
        self.path = []
        self.uiStatus = UIStatus.STARTWAHL

        self.recalc_button = Button("Neu Berechnen", 66, 700, 66, 33, self.batch)
        self.labels = [
            pyglet.text.Label('Weg', x=10, y=950, anchor_y='bottom',
                              color=(255, 255, 255, 255), batch=self.batch),
            pyglet.text.Label('Wiese', x=10, y=910, anchor_y='bottom',
                              color=(255, 255, 255, 255), batch=self.batch),
            pyglet.text.Label('Boot', x=10, y=870, 
                              anchor_y='bottom', color=(255, 255, 255, 255), 
                              batch=self.batch),
            pyglet.text.Label('Wald', x=10, y=830, 
                              anchor_y='bottom', color=(255, 255, 255, 255), 
                              batch=self.batch),
            pyglet.text.Label('Berg', x=10, y=790, 
                              anchor_y='bottom', color=(255, 255, 255, 255), 
                              batch=self.batch)
        ]

        self.widgets = [
            TextWidget(2, 100, 950, 100, self.batch),
            TextWidget(4, 100, 910, 100, self.batch),
            TextWidget(4, 100, 870, 100, self.batch),
            TextWidget(6, 100, 830, 100, self.batch),
            TextWidget(9, 100, 790, 100, self.batch)
        ]
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def get_color(self, i):
        # 0 Wasser, 1 Wiese, 2 Weg, 3 bergiges Gelände, 4 Wald
        if i == 0:
            return (10,30,200)
        elif i == 1:
            return (60,200,90)
        elif i == 2:
            return (200,150,150)
        elif i == 3:
            return (200,200,200)
        elif i == 4:
            return (0,100,0)
        else:
            return (0,0,0)
    
    def run(self):
        pyglet.app.run()

    def coord_to_window(self, x, y, centered):
        x_offset = 0
        y_offset = 1
        if centered:
            x_offset = 0.5
            y_offset = 0.5
        return self.parameter_input_width + (x+x_offset)*self.rect_width, self.height - (y+y_offset)*self.rect_width

    def set_start(self, x, y):
        self.goalTile = None
        self.path = None
        self.startTile = shapes.Circle(*self.coord_to_window(x,y,True),self.rect_width/2, color=(255,255,0), batch=self.batch)
    
    def set_goal(self, x, y):
        self.goalTile = shapes.Circle(*self.coord_to_window(x,y,True),self.rect_width/2, color=(255,0,0), batch=self.batch)

    def draw_path(self, points):
        path = []
        rect_width = self.rect_width
        for i in range(len(points)-1):
            start = points[i].point
            end = points[i+1].point
            path.append(shapes.Line(*self.coord_to_window(start.x,start.y, True), 
                             *self.coord_to_window(end.x,end.y, True), width=5, color=(200,50,50), batch=self.batch))
        self.path = path


    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)
            if button & mouse.LEFT and x > self.parameter_input_width:
                if x < self.parameter_input_width:
                    return
                if self.uiStatus == UIStatus.STARTWAHL:
                    self.startPoint = Point(int((x-self.parameter_input_width)/self.rect_width), int((self.height-y)/self.rect_width))
                    self.set_start(self.startPoint.x, self.startPoint.y)
                    self.uiStatus = UIStatus.ZIELWAHL
                elif self.uiStatus == UIStatus.ZIELWAHL:
                    self.goalPoint = Point(int((x-self.parameter_input_width)/self.rect_width), int((self.height-y)/self.rect_width))
                    self.set_goal(self.goalPoint.x, self.goalPoint.y)
                    self.uiStatus = UIStatus.STARTBERECHNUNG
            if self.recalc_button.hit_test(x,y) and self.uiStatus == UIStatus.STARTWAHL and self.startTile != None and self.goalTile != None:
                self.uiStatus = UIStatus.STARTBERECHNUNG

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)
            self.update_params()

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)
            self.update_params()

    def update_params(self):
        try:
            self.parameters.t_weg = int(self.widgets[0].document.text)
            self.parameters.t_wiese = int(self.widgets[1].document.text)
            self.parameters.t_boot = int(self.widgets[2].document.text)
            self.parameters.t_wald = int(self.widgets[3].document.text)
            self.parameters.t_berg = int(self.widgets[4].document.text)
        except ValueError:
            print("value error")
      
    def on_text_motion_select(self, motion):
        if self.focus:
            print("text motion select")
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        
    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


class TextWidget(object):
    def __init__(self, start_value: int, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(str(start_value))
        self.document.set_style(0, len(self.document.text), 
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class Button(object):
    def __init__(self, text, x, y, width, height, batch):
        self.rect = Rectangle(x,y,x+width,y+height, batch)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def hit_test(self, x, y):
        return (0 < x - self.x < self.width and
                0 < y - self.y < self.height)


class Rectangle(object):
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )