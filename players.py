from os import system
import board
from time import time

class ship:
    def __init__(self, length, rotation, start_x, start_y):
        self.rotation = rotation.lower()
        self.length = length
        self.start_x = start_x-1
        self.start_y = start_y-1
    
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
    def __init__(self, playerboard=board.board(), ship_types=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        self.playerboard=playerboard
        self.ship_types = ship_types

    def check_legal_placement(self, ship_coordinates):
        #Checks for colliding coordinates
        for coordinate in ship_coordinates:
            if (coordinate[0] > self.playerboard.x or coordinate[0] <= 0) or (coordinate[1] > self.playerboard.y or coordinate[1] <= 0):
                return False
            for occupied_coordinate in self.playerboard.players_ships:
                if coordinate in occupied_coordinate:
                    return False
        return True
        

class human(player):
    def place_ships(self):
        for ship_type in self.ship_types:
            system("cls")
            self.playerboard.print_board()
            while True:
                ship_start_location = input(f"Place ship with {ship_type} blocks (x, y, e.g right)")
                ship_x, ship_y, ship_rotation = ship_start_location.split(",")

                playership = ship(ship_type, ship_rotation, int(ship_x), int(ship_y))
                if self.check_legal_placement(playership.get_coordinates()):
                    self.playerboard.players_ships.append(playership.get_coordinates())
                    self.playerboard.populate_board()
                    break
                else:
                    print("Collision detected")
                    



class ai(player):
    def __init__(self, playerboard=board.board(), ship_types=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]):
        super().__init__(playerboard, ship_types)

    def place_ships(self):
        
        for ship_type in self.ship_types:
            self.playerboard.print_board()
            ship_start_location = input(f"Place ship with {ship_type} blocks (x, y, e.g right)")
            ship_x, ship_y, ship_rotation = ship_start_location.split(",")

            ship = ship(ship_type, ship_rotation, int(ship_x), int(ship_y))
            self.playerboard.players_ships.append(ship.get_coordinates())
            self.playerboard.populate_board()
            system("cls")
