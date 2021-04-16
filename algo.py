
from queue import PriorityQueue
from enum import Enum

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

class BootStatus(Enum):
    VERFUEGBAR = 0
    SCHWIMMT = 1
    VERBRAUCHT = 2

class A_Star:
    def __init__(self, board):
        #Reißekosten TODO v umbenennen
        self.v_weg = 2
        self.v_wiese_boot = 4
        self.v_wald = 6
        self.v_berg = 9
        self.v_nicht_begehbar = 10000 #todo biggest int
        self.board = board
        
    # Manhattan distanz
    def dist(self, a: Point, b: Point):
        return abs(a.x-b.x) + abs(a.y-b.y)

    # Die Kosten auf eine Kachel zu reißen hängen vom Typ der Zielkachel ab
    # Je nach dem wie schnell man auf der Kachel reißt, unterscheiden sich die Kosten der Kachel
    # Wenn ein Boot verfügbar ist, kann dies benutzt werde, sindder Status geht auf 'SCHWIMMT'
    # Wenn man schon im Wasser ist (SCHWIMMT), kann man weiter auf dem Wasser fahren, oder an Land gehen
    # Geht man nach dem Status 'SCHWIMMT' an Land ist der boot_status 'VERBRAUCHT', das Boot kann nicht mehr genutzt werden
    def kosten(self, a: Point, boot_status: BootStatus): 
        feld = self.board[a.y][a.x]
        if feld == 0: # Wasser
            if boot_status == BootStatus.VERFUEGBAR:
                return self.v_wiese_boot, BootStatus.SCHWIMMT
            elif boot_status == BootStatus.SCHWIMMT:
                return self.v_wiese_boot, BootStatus.SCHWIMMT
            elif boot_status == BootStatus.VERBRAUCHT:
                return self.v_nicht_begehbar, BootStatus.VERBRAUCHT
            print("ERROR")
            return -1, 0
        else:
            if boot_status == BootStatus.SCHWIMMT:
                boot_status = BootStatus.VERBRAUCHT

            if feld == 1: # Wiese
                return self.v_wiese_boot, boot_status
            elif feld == 2: # Weg
                return self.v_weg, boot_status
            elif feld == 3: # bergiges Gelände
                return self.v_berg, boot_status
            elif feld == 4: # Wald
                return self.v_wald, boot_status
            else:
                print("ERROR")
                return -1, 0

    # gibt benachbarten Kacheln zurück links, rechts, oben, unten (solange kein Kartenrand)
    def nachbar(self, i: Point):
        neighbors = [Point(i.x+1,i.y),Point(i.x,i.y+1),Point(i.x-1,i.y),Point(i.x,i.y-1)]
        moin = [n for n in neighbors if n.x >= 0 and n.y >= 0 and n.x < len(self.board[0]) and n.y < len(self.board)]
        return moin


    def calc(self, start: Point, goal: Point):
        queue = PriorityQueue()
        queue.put((0, start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = (None, BootStatus.VERFUEGBAR)
        cost_so_far[start] = 0
        
        while not queue.empty():
            current = queue.get()
            currentPoint = current[1]
            if currentPoint == goal:
                break
            
            for p in self.nachbar(currentPoint):
                boot_status = came_from[currentPoint][1]
                k, boot_status = self.kosten(p, boot_status)
                new_cost = cost_so_far[currentPoint] + k
                if p not in cost_so_far or new_cost < cost_so_far[p]:
                    cost_so_far[p] = new_cost
                    priority = new_cost + self.dist(p, goal)
                    queue.put((priority, p))
                    came_from[p] = (currentPoint, boot_status)

        return came_from, cost_so_far

