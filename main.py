from _thread import start_new_thread
from algo import Point, PointBootStatus, A_Star, Params, BootStatus
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

if __name__=="__main__":
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
            ziel = vizu.goalPoint

            kommt_von, kosten_bis_punkt, ziel_mit_status = calculator.calc(start, ziel)


            path = []

            toTile = ziel_mit_status
            path.append(toTile)
            while toTile != PointBootStatus(start, BootStatus.VERFUEGBAR):
                fromTile = kommt_von[toTile]
                path.append(fromTile)
                toTile = fromTile
            path.reverse()

            vizu.draw_path(path)
            print("Günstigster Weg:", "->".join(str(x.point) for x in path))
            print("Gesamtkosten:", kosten_bis_punkt[ziel_mit_status])

            vizu.uiStatus = UIStatus.STARTWAHL


