from vizualisation import Vizu
from _thread import start_new_thread
from algo import Point, A_Star

def read_csv():
    board = []
    import csv
    with open('gelaende_002.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        x = 0
        y = 0
        for row in csv_reader:
            row_numbers = []
            for cell in row:
                if cell == '':
                    return board
                number = int(cell)
                row_numbers.append(number)
                x+=1
            board.append(row_numbers)

board = read_csv()
for y in board:
    for x in y:
        print(x, end=" ")
    print()

vizu = Vizu(board)
start_new_thread(vizu.run, () )

calculator = A_Star(board)
startTile = Point(0,20)
goalTile = Point(36 ,22)

from vizualisation import UIStatus
from pyglet.window import mouse
@vizu.event
def on_mouse_press(x, y, buttons, modifiers):
    global startTile, goalTile
    if buttons & mouse.LEFT:
        if vizu.uiStatus == UIStatus.STARTWAHL:
            startTile = Point(int(x/vizu.rect_width), int((vizu.height-y)/vizu.rect_width))
            vizu.set_start(startTile.x, startTile.y)
            vizu.uiStatus = UIStatus.ZIELWAHL
        elif vizu.uiStatus == UIStatus.ZIELWAHL:
            goalTile = Point(int(x/vizu.rect_width), int((vizu.height-y)/vizu.rect_width))
            vizu.set_goal(goalTile.x, goalTile.y)
            vizu.uiStatus = UIStatus.STARTBERECHNUNG

while True:
    if vizu.uiStatus == UIStatus.STARTBERECHNUNG:
        print("calc ", startTile, goalTile)
        came_from, cost_so_far = calculator.calc(startTile, goalTile)
        path = []
        toTile = goalTile
        path.append(toTile)
        while toTile != startTile:
            fromTile = came_from[toTile][0]
            path.append(fromTile)
            toTile = fromTile
        
        for p in path:
            print(p, end=" ")
        print()

        vizu.draw_path(path)
        vizu.uiStatus = UIStatus.STARTWAHL



