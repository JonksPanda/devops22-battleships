#creates an object for each coordinate
class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = None
    def print_coordinate(self):
        pass

class board:
    #x and y decides how many rows to add horisontally(x) and vertically(y) default is 10
    def __init__(self, x=10, y=10):
        self.x = x
        self.y = y

        #Lists all ships belonging to player
        self.players_ships = []

        
    def write_board(self):
        pass

if __name__ == "__main__":
    board().write_board()