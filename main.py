from vizualisation import Vizu
from queue import PriorityQueue

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def __lt__(self, other):
        return self.x + self.y < other.x + other.y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    def __hash__(self):
        return hash((self.x, self.y))

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

#Geschwindigkeiten
v_weg = 2
v_wiese_boot = 4
v_wald = 6
v_berg = 9
v_nicht_begehbar = 10000

# fluss ohne boot nicht überquerbar
# Einweg boot
# 0 Wasser, 1 Wiese, 2 Weg, 3 bergiges Gelände, 4 Wald

def dist(a: Point, b: Point):
    return abs(a.x-b.x) + abs(a.y-b.y)

def kosten(a: Point):
    feld = board[a.y][a.x]
    if feld == 0: # Wasser
        return v_nicht_begehbar
    elif feld == 1: # Wiese
        return v_wiese_boot
    elif feld == 2: # Weg
        return v_weg
    elif feld == 3: # bergiges Gelände
        return v_berg
    elif feld == 4: # Wald
        return v_wald
    else:
        print("ERROR")
        return -1

def nachbar(i: Point):
    neighbors = [Point(i.x+1,i.y),Point(i.x,i.y+1),Point(i.x-1,i.y),Point(i.x,i.y-1)]
    moin = [n for n in neighbors if n.x >= 0 and n.y >= 0 and n.x < len(board[0]) and n.y < len(board)]
    return moin


def a_star(board, start: Point, goal: Point):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        currentPoint = current[1]
        print("current",current[0],current[1], "kosten", kosten(currentPoint))
        if currentPoint == goal:
            break
        
        for p in nachbar(currentPoint):
            new_cost = cost_so_far[currentPoint] + kosten(p)
            print(p, new_cost)
            if p not in cost_so_far or new_cost < cost_so_far[p]:
                cost_so_far[p] = new_cost
                priority = new_cost + dist(p, goal)
                frontier.put((priority, p))
                came_from[p] = currentPoint

    return came_from, cost_so_far


startTile = Point(0,0)
goalTile = Point(39,40)
came_from, cost_so_far = a_star(board, startTile, goalTile)

print("fjkdlsa", kosten(Point(28,33)))

path = []
toTile = goalTile
path.append(toTile)
while toTile != startTile:
    fromTile = came_from[toTile]
    path.append(fromTile)
    toTile = fromTile

for p in path:
    print(p)

vizu = Vizu(board)
vizu.draw_path(path)
vizu.run()