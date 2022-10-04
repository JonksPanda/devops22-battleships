from os import system
import random
import board

default_shiptypes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

class ship:
    def __init__(self, length, rotation, start_x, start_y):
        self.rotation = rotation.lower()
        self.length = length
        self.start_x = start_x-1
        self.start_y = start_y-1
        self.coordinates = self.get_coordinates()
    
    def get_coordinates(self):
        coordinates = []
        if self.rotation == 'right':
            for x in range(self.length):
                coordinates.append((int(self.start_x)+x, int(self.start_y)))
        elif self.rotation == 'left':
            for x in range(self.length):
                coordinates.append((int(self.start_x)-x, int(self.start_y)))
        elif self.rotation == 'up':
            for y in range(self.length):
                coordinates.append((int(self.start_x), int(self.start_y)-y))
        elif self.rotation == 'down':
            for y in range(self.length):
                coordinates.append((int(self.start_x), int(self.start_y)+y))
        return coordinates


class player:
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes, playername="player 1"):
        self.playerboard=playerboard
        self.ship_types = ship_types
        self.playerships = []#playerboard.players_ships
        self.score = 0
        self.playername = playername

    #checks if out of bounds. Also checks if a coordinate is occupied if "placing_ships" is True
    def check_legal_placement(self, ship_coordinates, placing_ships=True):
        for coordinate in ship_coordinates:
            #Checks if coordinate is "out of bounds"
            if (coordinate[0] > self.playerboard.y or coordinate[0] < 0) or (coordinate[1] > self.playerboard.x or coordinate[1] < 0):
                return False
            #Checks for colliding coordinates
            if placing_ships:
                for occupied_coordinate in self.playerboard.players_ships:
                    if coordinate in occupied_coordinate:
                        return False
        return True
    
    def target_shot(self, x, y, opponent):
        #Flag to break out of nested loop
        hit = False

        for opponent_ship in opponent.playerboard.players_ships:
            for coordinate in opponent_ship:
                if coordinate == (x, y):
                    opponent.playerboard.boardlayout[y][x] = "X"
                    hit = True
                    self.score += 1
                    opponent_ship.remove(coordinate)
                    return hit
                else:
                    opponent.playerboard.boardlayout[y][x] = "*"
        return hit

class human(player):
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes):
        super().__init__(playerboard, ship_types)

    def place_ships(self):
        for ship_type in self.ship_types:
            system("cls")
            self.playerboard.print_board()
            while True:
                while True:
                    ship_start_location = input(f"Place ship with {ship_type} blocks (x, y, e.g right)")
                    try:
                        ship_x, ship_y, ship_rotation = ship_start_location.split(",")
                        ship_x = int(ship_x)
                        ship_y = int(ship_y)
                        if ship_rotation.lower() == 'right' or ship_rotation.lower() == 'left' or ship_rotation.lower() == 'down' or ship_rotation.lower() == 'up':
                            break
                        else:
                            print("Rotation not specified!")
                    except Exception:
                        print("incorrect input!")
                    
                
                if self.check_legal_placement(ship(ship_type, ship_rotation.lower(), int(ship_x), int(ship_y)).coordinates):
                    self.playerships.append(ship(ship_type, ship_rotation.lower(), int(ship_x), int(ship_y)))
                    self.playerboard.players_ships.append(self.playerships[len(self.playerships)-1].coordinates)
                    self.playerboard.populate_board()
                    break
                else:
                    print("Collision detected!")

class ai(player):
    def __init__(self, playerboard=board.board(), ship_types=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        super().__init__(playerboard, ship_types)
        self.playername = "CPU"
        

    def place_ships(self):
        system("cls")
        placements = ['right', 'left', 'down', 'up']
        #Only needs to randomize if no ships are loaded
        if len(self.playerships) == 0:
            for ship_type in self.ship_types:
                while True:
                    self.playerships.append(ship(ship_type, random.choice(placements), random.randint(0,9), int(random.randint(0,9))))
                    
                    if self.check_legal_placement(self.playerships[len(self.playerships)-1].coordinates):
                        self.playerboard.players_ships.append(self.playerships[len(self.playerships)-1].coordinates)
                        self.playerboard.populate_board() #for debugging only
                        break
            