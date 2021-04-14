from vizualisation import Vizu
from queue import PriorityQueue

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def __lt__(self, other):
        return self.x + self.y < other.x + other.y
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
for x in board:
    for y in x:
        print(y, end=" ")
    print()


#Geschwindigkeiten
v_weg = 9
v_wiese_boot = 6
v_berg = 4

# fluss ohne boot nicht überquerbar
# Einweg boot
# 0 Wasser, 1 Wiese, 2 Weg, 3 bergiges Gelände, 4 Wald

def dist(a: Point, b: Point):
    return abs(a.x-b.x) + abs(a.y-b.y)

def kosten(a: Point):
    feld = board[a.x][a.y]
    return 1

def nachbar(i: Point):
    neighbors = [Point(i.x+1,i.y),Point(i.x,i.y+1),Point(i.x-1,i.y),Point(i.x,i.y-1)]
    moin = [n for n in neighbors if n.x >= 0 and n.y >= 0 and n.x < len(board) and n.y < len(board[0])]
    return moin


def a_star(board, start: Point, goal: Point):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        print(current)
        if current == goal:
            break
        
        for next in nachbar(current):
            new_cost = cost_so_far[current] + kosten(next)
            print(next, new_cost)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + dist(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

came_from, cost_so_far = a_star(board, Point(7,7), Point(4,5))
print(came_from, cost_so_far)

vizu = Vizu(board)
path = [(1,5),(2,5),(2,6),(2,7),(1,7)]
vizu.draw_path(path)
vizu.run()