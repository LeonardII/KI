
from _thread import start_new_thread
from algo import Point, A_Star, Params


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

parameters = Params()

from vizualisation import Vizu, UIStatus
vizu = Vizu(board, parameters)
start_new_thread(vizu.run, () )

calculator = A_Star(board, parameters)

from pyglet.text import layout, caret, document, Label

y_offset = 1000 - 25
def add_edit_box(vizu: Vizu, name: str, start_value: int):
    global y_offset
    label = Label(name, font_name='Arial', x=10, y=y_offset, batch=vizu.batch)
    doc = document.FormattedDocument(text=str(start_value))
    doc.set_style(0,100, dict(font_name ='Arial', font_size = 16, color =(255, 255, 255, 255)))
    my_layout = layout.IncrementalTextLayout(doc,width=vizu.parameter_input_width/2, height=50, batch=vizu.batch)
    my_layout.x = vizu.parameter_input_width/2
    my_layout.y = y_offset - 32
    car = caret.Caret(my_layout, color=(255,255,255))
    vizu.push_handlers(car)
    y_offset -= 50


while True:
    if vizu.uiStatus == UIStatus.STARTBERECHNUNG:
        start = vizu.startPoint
        goal = vizu.goalPoint
        came_from, cost_so_far = calculator.calc(start, goal)
        path = []
        toTile = goal
        path.append(toTile)
        while toTile != start:
            fromTile = came_from[toTile][0]
            path.append(fromTile)
            toTile = fromTile
        path.reverse()

        vizu.draw_path(path)
        print("Günstigster Weg:", "->".join(str(x) for x in path))

        vizu.uiStatus = UIStatus.STARTWAHL


