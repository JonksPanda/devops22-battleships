from os import system
import board
from time import time

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
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes):
        self.playerboard=playerboard
        self.ship_types = ship_types
        self.playerships = playerboard.players_ships

    def check_legal_placement(self, ship_coordinates):
        for coordinate in ship_coordinates:
            #Checks if coordinate is "out of bounds"
            if (coordinate[0] > self.playerboard.x or coordinate[0] <= 0) or (coordinate[1] > self.playerboard.y or coordinate[1] <= 0):
                return False
            #Checks for colliding coordinates
            for occupied_coordinate in self.playerboard.players_ships:
                if coordinate in occupied_coordinate:
                    return False
        return True
    
    def target_shot(self, x, y, opponent):
        for opponent_ship in opponent.playerships:
            for coordinate in opponent_ship:
                if coordinate == (x, y):
                    opponent.playerboard.boardlayout[y][x] = "X"
                else:
                    opponent.playerboard.boardlayout[y][x] = "*"
        opponent.playerboard.print_board()

class human(player):
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes):
        super().__init__(playerboard, ship_types)

    def place_ships(self):
        for ship_type in self.ship_types:
            system("cls")
            self.playerboard.print_board()
            while True:
                ship_start_location = input(f"Place ship with {ship_type} blocks (x, y, e.g right)")
                ship_x, ship_y, ship_rotation = ship_start_location.split(",")

                self.playerships.append(ship(ship_type, ship_rotation, int(ship_x), int(ship_y)))
                if self.check_legal_placement(self.playerships[len(self.playerships)-1].coordinates):
                    self.playerboard.players_ships.append(self.playerships[len(self.playerships)-1].coordinates)
                    self.playerboard.populate_board()
                    break
                else:
                    print("Collision detected")

class ai(player):
    def __init__(self, playerboard=board.board(), ship_types=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        super().__init__(playerboard, ship_types)

    def place_ships(self):
        system("cls")
        
        #for ship_type in self.ship_types:
            # self.playerboard.print_board()
            # ship_start_location = input(f"Place ship with {ship_type} blocks (x, y, e.g right)")
            # ship_x, ship_y, ship_rotation = ship_start_location.split(",")

        ships = [ship(4, "right", 5, 4), ship(3, "down", 2, 1), ship(3, "up", 8, 9)]
        for aiship in ships:
            self.playerboard.players_ships.append(aiship.coordinates)
        self.playerboard.print_board()
            