import players
import board


class gamecontrol:
    def __init__(self):
        self.human_player = players.human()
        self.playerboard = board.board()
        self.ai = players.ai()

        #Let's players place ships on board on init
        self.human_player.place_ships()
        self.ai.place_ships()
    

    def gameloop(self):
        pass
    
if __name__ == "__main__":
    game = gamecontrol()
    game.gameloop()