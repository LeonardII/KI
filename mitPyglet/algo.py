from queue import PriorityQueue
from enum import Enum
import sys

class Point:
    '''Punkt mit x,y Koordinate'''
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

class PointBootStatus():
    '''Punkt und Bootstatus in einem Objekt'''
    def __init__(self, point: Point, boot_status: BootStatus):
        self.boot_status = boot_status
        self.point = point
    def __lt__(self, other):
        return self.point < other.point
    def __eq__(self, other):
        return self.boot_status == other.boot_status and self.point == other.point
    def __hash__(self):
        return hash((self.boot_status, self.point))
    def __str__(self):
        return " ["+str(self.point)+" "+str(self.boot_status)+"]"

class Params:
    '''
    Parameter für A_Star
    Kacheln haben unterschiedliche Reisegeschwindigkeiten(Kosten)
    Ein Parameterobjekt wird mit A_Star und Vizu geteilt um Parameter aus der GUI zu ändern
    '''
    def __init__(self):
        self.t_weg = 2
        self.t_wiese = 4
        self.t_boot = 4
        self.t_wald = 6
        self.t_berg = 9
        self.t_nicht_begehbar = sys.maxsize # Ist unendlich, bzw größer als jede andere Zahl


class A_Star:
    '''
    Beinhaltet den eigentlichen Algorithmus und Helferfunktionen
    '''
    def __init__(self, board, parameters: Params):
        self.board = board
        self.parameters = parameters
        
    # Manhattan distanz
    def dist(self, a: Point, b: Point):
        return abs(a.x-b.x) + abs(a.y-b.y)

    # Die Kosten auf eine Kachel zu reißen hängen vom Typ der Zielkachel ab
    # Je nach dem wie schnell man auf der Kachel reißt, unterscheiden sich die Kosten der Kachel
    # Wenn ein Boot verfügbar ist, kann dies benutzt werde, der Status geht auf 'SCHWIMMT'
    # Wenn man schon im Wasser ist (SCHWIMMT), kann man weiter auf dem Wasser fahren, oder an Land gehen
    # Geht man nach dem Status 'SCHWIMMT' an Land ist der boot_status 'VERBRAUCHT', das Boot kann nicht mehr genutzt werden
    def kosten(self, ziel: Point, boot_status: BootStatus) -> (int, BootStatus): 
        feld = self.board[ziel.y][ziel.x]
        if feld == 0: # Wasser
            if boot_status == BootStatus.VERFUEGBAR:
                return self.parameters.t_boot, BootStatus.SCHWIMMT
            elif boot_status == BootStatus.SCHWIMMT:
                return self.parameters.t_boot, BootStatus.SCHWIMMT
            elif boot_status == BootStatus.VERBRAUCHT:
                return self.parameters.t_nicht_begehbar, BootStatus.VERBRAUCHT
            print("ERROR")
            return -1, 0
        else:
            if boot_status == BootStatus.SCHWIMMT:
                boot_status = BootStatus.VERBRAUCHT

            if feld == 1: # Wiese
                return self.parameters.t_wiese, boot_status
            elif feld == 2: # Weg
                return self.parameters.t_weg, boot_status
            elif feld == 3: # bergiges Gelände
                return self.parameters.t_berg, boot_status
            elif feld == 4: # Wald
                return self.parameters.t_wald, boot_status
            else:
                print("ERROR")
                return -1, 0

    # gibt benachbarten Kacheln zurück links, rechts, oben, unten (solange kein Kartenrand)
    def nachbar(self, p: Point):
        neighbors = [Point(p.x+1,p.y),Point(p.x,p.y+1),Point(p.x-1,p.y),Point(p.x,p.y-1)]
        punkte_innerhalb_karte = [n for n in neighbors if n.x >= 0 and n.y >= 0 and n.x < len(self.board[0]) and n.y < len(self.board)]
        return punkte_innerhalb_karte

    # a star Algorithmus
    def calc(self, startPoint: Point, zielPoint: Point):
        print("Berechne kürzesten Weg von",startPoint,"nach",zielPoint,"\nmit den Parametern",vars(self.parameters))

        # PriorityQueue ist ein Heap, welcher immer Punkt mit der kleinsten Priorität ausgeben kann
        queue = PriorityQueue()
        start = PointBootStatus(startPoint,BootStatus.VERFUEGBAR)
        if self.board[startPoint.y][startPoint.x] == 0:
            start = PointBootStatus(startPoint,BootStatus.SCHWIMMT)
        queue.put((0, start))

        kommt_von = dict()
        kommt_von[start] = PointBootStatus(None, BootStatus.VERFUEGBAR)

        kosten_bis_punkt = dict()
        kosten_bis_punkt[start] = 0
        
        currentPoint = None
        while not queue.empty():
            currentPoint = queue.get()[1]

            if currentPoint.point == zielPoint:
                break # Ziel gefunden
            
            boot_status = currentPoint.boot_status

            # Nachbarpunkte werden untersucht
            for p in self.nachbar(currentPoint.point):
                p_kosten, p_boot_status = self.kosten(p, boot_status)
                p_gesamt_kosten = kosten_bis_punkt[currentPoint] + p_kosten
                p_mit_boot_status = PointBootStatus(p, p_boot_status)
                
                # Nachbarpunkt wird in dicts und queue aufgenommen, oder seine Kosten aktuallisiert, wenn ein billigerer Pfad gefunden wurde
                if p_mit_boot_status not in kosten_bis_punkt or p_gesamt_kosten < kosten_bis_punkt[p_mit_boot_status]:
                    kosten_bis_punkt[p_mit_boot_status] = p_gesamt_kosten

                    # Priorität sind hier die Gesamtkosten + Abstand zum Ziel
                    priority = p_gesamt_kosten + self.dist(p, zielPoint)
                    queue.put((priority, p_mit_boot_status))
                    kommt_von[p_mit_boot_status] = currentPoint

        ziel = currentPoint
        return kommt_von, kosten_bis_punkt, ziel

