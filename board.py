import players

#creates an object for each coordinate
class board:
    #x and y decides how many rows to add horisontally(x) and vertically(y) default is 10
    def __init__(self, x=10, y=10):
        self.x = x
        self.y = y
        #Stores the visible board
        self.boardlayout = []
        #Lists all ships coordinates belonging to player
        self.players_ships = []
        self.generate_board()

    def generate_board(self):
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row.append("O")
            self.boardlayout.append(row)    

    
    def populate_board(self):
        for ship in self.players_ships:
            for coordinate in ship:
                self.boardlayout[coordinate[1]][coordinate[0]] = chr(9608)


    def print_board(self):
        print(['1','2','3','4','5','6','7','8','9','10'])
        print('\n'.join(map(str, self.boardlayout))) #Code used from https://github.com/fictive-reality/devops22-python/blob/master/lesson_6/examples/7_copy.py

if __name__ == "__main__":

    player_board = board()
    player_board.generate_board()
    #player_board.print_board()
    player_board.populate_board()
    player_board.print_board()