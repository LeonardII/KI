from _thread import start_new_thread
from algo import Point, PointBootStatus, A_Star, Params, BootStatus

def read_csv(file):
    board = []
    import csv
    with open(file, encoding='utf-8-sig') as csv_file:
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
    return board

def get_int(default: int) -> int:
    while True:
        i = input()
        if isinstance(i, str) and len(i) == 0:
            return default
        if int(i):
            return int(i)

def get_str() -> str:
    while True:
        i = input()
        if isinstance(i, str):
            return str(i)

def get_char(i):
        # 0 Wasser, 1 Wiese, 2 Weg, 3 bergiges Gelände, 4 Wald
        if i == 0:
            return '~'
        elif i == 1:
            return '░'
        elif i == 2:
            return '▩'
        elif i == 3:
            return '▒'
        elif i == 4:
            return '▥'

def path_vizu(path, board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if Point(x, y) in path:
                print("█", end=" ")
            else:
                print(get_char(board[y][x]), end=" ")
        print()

if __name__=="__main__":

    # CSV Einlesen
    print("Board CSV Pfad (default 'gelaende_002.csv')")
    file_path = get_str()
    if len(file_path) == 0:
        file_path = "gelaende_002.csv"
    board = read_csv(file_path)
    for y in range(len(board)):
        for x in range(len(board[y])):
            print(get_char(board[y][x]), end=" ")
        print()

    # Parameter für den Algorithmus initialisieren
    print("Parameter bearbeiten:")
    parameters = Params()
    print("Weg (default",str(parameters.t_weg)+')')
    parameters.t_weg = get_int(parameters.t_weg)
    print("Wiese (default",str(parameters.t_wiese)+')')
    parameters.t_wiese = get_int(parameters.t_wiese)
    print("Boot (default",str(parameters.t_boot)+')')
    parameters.t_boot = get_int(parameters.t_boot)
    print("Wald (default",str(parameters.t_wald)+')')
    parameters.t_wald = get_int(parameters.t_wald)
    print("Berg (default",str(parameters.t_berg)+')')
    parameters.t_berg = get_int(parameters.t_berg)

    print("Startpunkt X (default 1)")
    start_x = get_int(1)
    print("Startpunkt Y (default 1)")
    start_y = get_int(1)
    print("Zielpunkt X (default 30)")
    ziel_x = get_int(30)
    print("Zielpunkt Y (default 38)")
    ziel_y = get_int(38)

    # Algorithmusrechner initialisieren
    calculator = A_Star(board, parameters)

    start = Point(start_x, start_y)
    ziel = Point(ziel_x, ziel_y)

    # A Stern ausführen
    kommt_von, kosten_bis_punkt, ziel_mit_status = calculator.calc(start, ziel)

    # Pfad aus dict erstellen
    path = []
    toTile = ziel_mit_status
    path.append(toTile)
    while toTile != PointBootStatus(start, BootStatus.VERFUEGBAR):
        fromTile = kommt_von[toTile]
        path.append(fromTile)
        toTile = fromTile
    path.reverse()
    
    point_path = [x.point for x in path]

    # Pfad visualisieren, ausgeben
    path_vizu(point_path, board)
    print("Günstigster Weg:", "->".join(str(x.point) for x in path))
    print("Gesamtkosten:", kosten_bis_punkt[ziel_mit_status])



