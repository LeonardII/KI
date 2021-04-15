
import pyglet
from pyglet import shapes

class Vizu(pyglet.window.Window):
    def __init__(self, board):
        super().__init__(width=1000, height=1000)
        self.batch = pyglet.graphics.Batch()
        self.b = []

        # (40,40) to (1000,1000)
        self.rect_width = 1000/42
        rect_width = self.rect_width
        i = 0
        for row in board:
            for cell in row:
                number = int(cell)
                self.b.append(shapes.Rectangle((i%40)*rect_width, self.height - int(1+i/40)*rect_width, rect_width, rect_width, color=self.get_color(number), batch=self.batch))
                i+=1


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

    def draw_path(self, points):
        self.path = []
        rect_width = self.rect_width
        for i in range(len(points)-1):
            start = points[i]
            end = points[i+1]
            self.path.append(shapes.Line((start.x+.5)*rect_width, self.height-(start.y+.5)*rect_width, 
                             (end.x+.5)*rect_width, self.height-(end.y+.5)*rect_width, width=5, color=(200,50,50), batch=self.batch))



    
