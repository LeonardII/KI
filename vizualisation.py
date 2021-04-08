
import pyglet
from pyglet import shapes

class Vizu(pyglet.window.Window):
    def __init__(self, board):
        self.batch = pyglet.graphics.Batch()
        self.b = []

        # (40,40) to (1000,1000)
        rect_width = 1000/42
        i = 0
        for row in board:
            for cell in row:
                number = int(cell)
                self.b.append(shapes.Rectangle((i%40)*rect_width, int(i/40)*rect_width, rect_width, rect_width, color=self.get_color(number), batch=self.batch))
                i+=1

        super().__init__(width=1000, height=1000)
        pyglet.app.run()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def get_color(self, i):
        # 0 Wasser, 1 Wiese, 2 Weg, 3 bergiges Gelände, 4 Wald
        if i == 0:
            return (10,30,200)
        elif i == 1:
            return (10,200,30)
        elif i == 2:
            return (200,150,150)
        elif i == 3:
            return (200,200,200)
        elif i == 4:
            return (10,200,20)
        else:
            return (0,0,0)


    
