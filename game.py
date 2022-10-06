import players
import os
import menu
import stats


class gamecontrol:
    def __init__(self, player1 = players.human(), player2 = players.ai()):
        #adds players to the game
        self.player1 = player1
        self.player2 = player2
        self.show_ai_board = False
        #adds stats class to store statistics. Creates SQL-connection on init
        self.stats = stats.stats()
        self.winner = ''
        self.end = False
        self.win_score = 20
        

        #Let's players place ships on board on init

        self.turn = 0

    #Let's player choose some options and name
    def prepare_game(self):
        os.system("cls")
        print(f"""
1. change name (Current: {self.player1.playername}) 
2. load AI ship-template (current: {self.player2.template})
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
        #returns to main menu
        elif choice == "4":
            menu.main()
        #loads this menu again if wrong input
        else:
            self.prepare_game()



    #prints the game current interface. Also used for updating the screen 
    def interface(self):
            os.system("cls")
            print(f"turn: {self.turn} | {self.player1.playername}: {self.player1.score}/{self.win_score} | {self.player2.playername}: {self.player2.score}/{self.win_score}")
            print(f"{self.player1.playername}:")
            self.player1.playerboard.print_board()
            print("__________________________________________________")
            print(f"{self.player2.playername}:")
            self.player2.playerboard.print_board()
            print(f"""
Legend:
    O = Empty spot
    X = Hit
    * = Miss
    {chr(9608)} = ship         
            """)

    def check_win(self, player):
        if player.score >= self.win_score:
            self.winner = player.playername
            self.end = True
            return True
        return False

    def gameloop(self):
        #flag to break out of nestled loop
        while True: 
            self.turn += 1
            #Player1s turn
            while True:
                self.interface()
                if self.player1.turn(self.player2):
                #breaks loop before next turn begins if winner is decided
                    if self.check_win(self.player1):
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
                    if self.check_win(self.player2):
                        break
                else:
                    break

            #breaks loop before next turn begins if winner is decided
            if self.end:
                self.interface()
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
        print("Do you want to play again? (y/n)")
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