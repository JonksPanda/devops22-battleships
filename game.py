import players
import random
import os
import time


class gamecontrol:
    def __init__(self):
        self.human_player = players.human()
        self.ai = players.ai()

        #Let's players place ships on board on init
        self.human_player.place_ships()
        self.human_player.playerboard.populate_board()
        self.ai.place_ships()

    def interface(self):
            os.system("cls")
            print("AI:")
            self.ai.playerboard.print_board()
            print("__________________________________________________")
            print("Player 1:")
            self.human_player.playerboard.print_board()

    def gameloop(self):
        while True: 
            self.interface()
            target_x, target_y = input("Player 1: Choose a coordinate to shoot").split(",")
            self.human_player.target_shot(int(target_x)-1, int(target_y)-1, opponent=self.ai)
            self.interface()
            print("AI: turn in progress..")
            #Compare players score if there's any winner yet.
            #waits 3 seconds to make it seem like the AI has to "think"
            time.sleep(3)
            self.ai.target_shot(random.randint(0,9), random.randint(0,9), opponent=self.human_player)
            #Compare players score again if there's any winner yet.
            #If anyone have won, announce the winner and return to main menu
            
    
if __name__ == "__main__":
    game = gamecontrol()
    game.gameloop()