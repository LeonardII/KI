
import pyglet
from pyglet import shapes
from enum import Enum

class UIStatus(Enum):
    STARTWAHL = 0
    ZIELWAHL = 1
    STARTBERECHNUNG = 2

class Vizu(pyglet.window.Window):
    def __init__(self, board):
        self.parameter_input_width = 200
        super().__init__(width=1000 + self.parameter_input_width, height=1000)
        
        self.batch = pyglet.graphics.Batch()
        self.b = []

        # (40,40) to (1000,1000)
        self.rect_width = 1000/42
        i = 0
        for row in board:
            for cell in row:
                number = int(cell)
                self.b.append(shapes.Rectangle(*self.coord_to_window((i%40), int(i/40), False),self.rect_width, self.rect_width, color=self.get_color(number), batch=self.batch))
                i+=1
        
        self.startTile = None
        self.goalTile = None
        self.path = []
        self.uiStatus = UIStatus.STARTWAHL

    def on_draw(self):
        print("redraw")
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
        print("Run ")
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
            start = points[i]
            end = points[i+1]
            path.append(shapes.Line(*self.coord_to_window(start.x,start.y, True), 
                             *self.coord_to_window(end.x,end.y, True), width=5, color=(200,50,50), batch=self.batch))
        self.path = path