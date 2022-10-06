import players
import os
import time
import menu
import stats


class gamecontrol:
    def __init__(self, player1 = players.human(), player2 = players.ai()):
        #adds players to the game
        self.player1 = player1
        self.player2 = player2
        #adds stats class to store statistics
        self.stats = stats.stats()
        self.winner = ''
        self.end = False

        #Let's players place ships on board on init

        self.turn = 0

    #Let's player choose some options and name
    def prepare_game(self):
        os.system("cls")
        print(f"""
1. change name (Current: {self.player1.playername}) 
2. load player2 ship-template (current: {self.player2.template})
3. start game
4. exit to menu
        """)
        choice = input("Select an option from the list: ")
        #change name
        if choice == "1":
            os.system("cls")
            self.player1.playername = input("Input your name: ").capitalize()
            if self.player1.playername == "":
                self.player1.playername = "Player 1"
            self.prepare_game()
        #Load template
        elif choice == "2":
            os.system("cls")
            while True:
                #list files to choose from
                self.player2.load_ship_placements()
                break
            self.prepare_game()
        #starts game and lets player prepare board
        elif choice == "3":
            os.system("cls")
            self.player1.place_ships()
            self.player1.playerboard.populate_board()
            self.player2.place_ships()
            return
        #returns to mainn menu
        elif choice == "4":
            menu.main()
        #loads this menu agplayer2n if wrong input
        else:
            self.prepare_game()



    #prints the game current interface. Also used for updating the screen 
    def interface(self):
            os.system("cls")
            print(f"turn: {self.turn} | {self.player1.playername}: {self.player1.score}/{20} | {self.player2.playername}: {self.player2.score}/{20}")
            print(f"{self.player1.playername}:")
            self.player1.playerboard.print_board()
            print("__________________________________________________")
            print(f"{self.player2.playername}:")
            self.player2.playerboard.print_board()

    def gameloop(self):
        #flag to break out of nestled loop
        while True: 
            self.turn += 1
            #Player1s turn
            while True:
                self.interface()
                if self.player1.turn(self.player2):
                #breaks loop before next turn begins if winner is decided
                    if self.player1.score >= 20:
                        self.winner = self.player1.playername
                        self.end = True
                        break
                else:
                    break

            if self.end:
                print(f"{self.winner} has won!")
                break

            #player2s turn
            while True:
                self.interface()
                if self.player2.turn(self.player1):
                #breaks loop before next turn begins if winner is decided
                    if self.player2.score >= 20:
                        self.winner = self.player2.playername
                        self.end = True
                        break
                else:
                    break

            #breaks loop before next turn begins if winner is decided
            if self.end:
                print(f"{self.winner} has won!")
                break
        #Saves stats to database /data/game_data.db
        self.stats.save_stats(self.winner, self.turn)    
        
    #saves players board layout to file that can be used as player2s layout in another game
    def save_board_layout(self):
        print("Would you like to save your board-layout as template? (y/n)")
        while True:
            answer = input("answer: ")
            if answer.lower() == "y":
                self.player1.save_ship_placement()
                break
            elif answer.lower() == "n":
                break
            else:
                print("incorrect input!")
    
    def restart(self):
        os.system("cls")
        print("Do you want to play agplayer2n? (y/n)")
        answer = input("answer: ")
        if answer.lower() == "y":
            main()
        elif answer.lower() == "n":
            menu.main()
        else:
            print("incorrect input!")

def main():
    game = gamecontrol()
    game.prepare_game()
    game.gameloop()
    game.save_board_layout()
    game.restart()


if __name__ == "__main__":
    main()