import os
import random
import board
import json
import time
import main

default_shiptypes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

class ship:
    def __init__(self, length, rotation, start_x, start_y):
        self.rotation = rotation.lower()
        self.length = length
        self.start_x = start_x
        self.start_y = start_y
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
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes, playername=""):
        self.playerboard=playerboard
        self.ship_types = ship_types
        self.playerships = [] #stores instances of ship-objects
        self.score = 0
        self.playername = playername
        self.targets_hit = [] #stores all targets hit

        #stores previous targets
        self.target_x_store = int()
        self.target_y_store = int()


    #checks if out of bounds. Also checks if a coordinate is occupied if "placing_ships" is True
    #ship_coordinates is expected to contain a list of tuples with coordinates
    def check_legal_placement(self, ship_coordinates, placing_ships=True):
        for coordinate in ship_coordinates:
            #Checks if coordinate is "out of bounds"
            if (coordinate[0] > self.playerboard.x-1 or coordinate[0] <= -1) or (coordinate[1] > self.playerboard.y-1 or coordinate[1] <= -1):
                return False
            #Checks for colliding coordinates in ship-placement-phase
            if placing_ships:
                for occupied_coordinates in self.playerboard.players_ships:
                    #checks if any of the new coordinates are already occupied
                    if coordinate in occupied_coordinates:
                        return False
                    #checks if any ajdacent coordinates are occupied
                    elif ((coordinate[0] + 1, coordinate[1]) in occupied_coordinates) or ((coordinate[0] - 1, coordinate[1]) in occupied_coordinates) or ((coordinate[0], coordinate[1] + 1) in occupied_coordinates) or ((coordinate[0], coordinate[1] - 1) in occupied_coordinates):
                        return False
            #checks if coordinate is already hit if it's not in ship-placement phase
            else:
                if coordinate in self.targets_hit:
                    return False
        #returns true only if none of the conditions above are met
        return True
    
    def target_shot(self, x, y, opponent):
        #Flag to break out of nested loop
        hit = False

        #checks if any of the opponents ships are the same as input
        for opponent_ship in opponent.playerboard.players_ships:
            if (x, y) in opponent_ship:
                opponent.playerboard.boardlayout[y][x] = "X"
                hit = True
                self.score += 1
                opponent_ship.remove((x,y))
                #breaks loop when coordinate matches an opponents coordinate
                break
            else:
                opponent.playerboard.boardlayout[y][x] = "*"
        #adds coordinate to list of coordinates shot at
        self.targets_hit.append((x, y))
        return hit

class human(player):
    def __init__(self, playerboard=board.board(), ship_types=default_shiptypes, playername="Player 1"):
        super().__init__(playerboard, ship_types, playername)

    def place_ships(self):
        for ship_type in self.ship_types:
            os.system("cls")
            self.playerboard.print_board()
            while True:
                while True:
                    try:
                        #Gets the starting position of the ship and rotation
                        ship_x, ship_y, ship_rotation = (input(f"Place ship with {ship_type} blocks (x,y,*direction* (ex. 5,2,right))").replace(" ", "")).split(",")
                        ship_x = int(ship_x)-1
                        ship_y = int(ship_y)-1
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
                    print("Illegal move!")
    def save_ship_placement(self):
        i = 0
        ships = []
        #Fetches all the ships from players fleet
        for ship in self.playerships:
            i += 1
            data = {
                    "x": ship.start_x,
                    "y": ship.start_y,
                    "length": ship.length,
                    "rotation": ship.rotation
                }
            ships.append(data)
        while True:
            template_name = input("input template-name: ")
            #prevents player to leave template_name empty
            if template_name != "":
                break
        json_path = f"{os.path.dirname(os.path.realpath(__file__))}\\data\\fleets\\{template_name}.json"
        fleet = {"fleet":ships}
        with open(json_path, 'w') as file:
            file.write(json.dumps(fleet, indent=4))

    def turn(self, opponent):
        #Expecting input x,y
        while True:
            player_input = input("Player 1: Choose a coordinate to shoot (x,y) or Type exit to exit game: ").replace(" ","")
            if player_input.lower() == "exit":
                main.main()
            try:
                target_x, target_y = player_input.split(",")
                target_x = int(target_x)-1
                target_y = int(target_y)-1
                if self.check_legal_placement([(target_x, target_y)], placing_ships=False):
                    #checks if player makes a hit and continues turn until player misses
                    if self.target_shot(target_x, target_y, opponent):
                        return True
                    else:
                        return False
            except Exception:
                print("Incorrect input!")

class ai(player):
    def __init__(self, playerboard=board.board(), ship_types=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1], playername="CPU"):
        super().__init__(playerboard, ship_types, playername)
        self.playername = playername
        self.template = "random"
        #True if last shot was successfull
        self.hit = False

    def load_ship_placements(self):
        #https://www.geeksforgeeks.org/read-json-file-using-python/
        while True:
            try:
                dir = f"{os.path.dirname(os.path.realpath(__file__))}\\data\\fleets\\"
                #prints the directory where templates is stored
                #https://pynative.com/python-list-files-in-a-directory/#h-os-scandir-to-get-files-of-a-directory
                for dir_file in os.scandir(dir):
                    if dir_file.is_file() and dir_file.name.endswith(".json"):
                        print(dir_file.name[:-5:])
                self.template = input("Choose template to load (leave empty for random): ")
                if self.template == "":
                    self.template = "random"
                    break
                json_path = f"{dir}{self.template}.json"
                file = open(json_path)
                data = json.load(file)
                for playership in data['fleet']:
                    self.playerships.append(ship(playership["length"], playership["rotation"], playership["x"], playership["y"]))
                break
            except Exception:
                print("Error loading file")
            os.system("cls")
        
    def place_ships(self):
        os.system("cls")
        rotations = ['right', 'left', 'down', 'up']
        #Only needs to randomize if no ships are loaded
        if len(self.playerships) == 0:
            for ship_type in self.ship_types:
                while True:
                    rotation = random.choice(rotations)
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                    
                    if self.check_legal_placement(ship(ship_type, rotation, x, y).coordinates):
                        self.playerships.append(ship(ship_type, rotation, x, y))
                        self.playerboard.players_ships.append(self.playerships[len(self.playerships)-1].coordinates)
                        break
        #fills playerboard if ships are already loaded
        else:
            for playership in self.playerships: 
                self.playerboard.players_ships.append(playership.coordinates)
        #self.playerboard.populate_board() #for debugging only
    
    def turn(self, opponent):
        #Storing the coordinates before the loop to make it easier to manipulate
        print(f"{self.playername}: turn in progress..")
        #If previous turn was successful, AI tries to shot next to the previous coordinate
        if self.hit:
            target_x = self.target_x_store
            target_y = self.target_y_store
            #stores all coordinates that player have tried
            coordinates_tried = []
            i = 1
            while True:
                #decides player2s next move
                decider = random.randint(1,4)
                if decider == 1:
                    if (self.check_legal_placement([(target_x + i, target_y)], placing_ships=False)):
                        target_x += i
                        break
                elif decider == 2:
                    if self.check_legal_placement([(target_x - i, target_y)], placing_ships=False):
                        target_x -= i
                        break
                elif decider == 3:
                    if self.check_legal_placement([(target_x, target_y + i)], placing_ships=False):
                        target_y += i
                        break
                elif decider == 4:
                    if self.check_legal_placement([(target_x, target_y - i)], placing_ships=False):
                        target_y -= i
                        break
                if (target_x, target_y) not in coordinates_tried and target_x:
                    coordinates_tried.append((target_x, target_y))
                elif len(coordinates_tried) == 4:
                    i += 1
                    coordinates_tried = []

        else:
            while True:
                target_x = random.randint(0,9)
                target_y = random.randint(0,9)
                if self.check_legal_placement([(target_x, target_y)], placing_ships=False):
                    break
        #put a sleep to make it easier to see player2s turn and make it seem like it's "thinking" https://realpython.com/python-sleep/
        time.sleep(1)
        #checks if player2 makes a hit and continues turn until player2 misses
        if self.target_shot(target_x, target_y, opponent):
            self.target_x_store = target_x
            self.target_y_store = target_y
            self.hit = True
            return True
        else:
            self.hit = False
            return False
            