from _thread import start_new_thread
from algo import Point, A_Star, Params
from vizualisation import Vizu, UIStatus

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

vizu = Vizu(board, parameters)
start_new_thread(vizu.run, () )

calculator = A_Star(board, parameters)

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


