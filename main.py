from vizualisation import Vizu


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

def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def kosten(a):
    return board[a[0], a[1]]

def nachbar(i):
    return [(i[0]+1,i[1]),(i[0],i[1]+1),(i[0]-1,i[1]),(i[0],i[1]-1)]

def a_star(board, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in nachbar(current):
            new_cost = cost_so_far[current] + kosten(next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + dist(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

#came_from, cost_so_far = a_star(board, (2,2), (10,9))
#print(came_from, cost_so_far)

vizu = Vizu(board)