import players
import random
import os
import time
import menu
import stats


class gamecontrol:
    def __init__(self):
        #adds players to the game
        self.human_player = players.human()
        self.ai = players.ai()
        #adds stats class to store statistics
        self.stats = stats.stats()

        #Let's players place ships on board on init

        self.turn = 0

    #Let's player choose some options and name
    def prepare_game(self):
        os.system("cls")
        print(f"""
1. change name (Current: {self.human_player.playername}) 
2. load AI ship-template (current: {self.ai.template})
3. start game
4. exit to menu
        """)
        choice = input("Select an option from the list: ")
        #change name
        if choice == "1":
            os.system("cls")
            self.human_player.playername = input("Input your name: ").capitalize()
            if self.human_player.playername == "":
                self.human_player.playername = "Player 1"
            self.prepare_game()
        #Load template
        elif choice == "2":
            os.system("cls")
            while True:
                #list files to choose from
                self.ai.load_ship_placements()
                break
            self.prepare_game()
        #starts game and lets player prepare board
        elif choice == "3":
            os.system("cls")
            self.human_player.place_ships()
            self.human_player.playerboard.populate_board()
            self.ai.place_ships()
            return
        #returns to main menu
        elif choice == "4":
            menu.main()
        #loads this menu again if wrong input
        else:
            self.prepare_game()

    def check_win(self, current_player):
        #Checks if score is more than or equals opponents amount of ships in fleet
        if current_player.score >= 20:
            return True
        else:
            return False

    #prints the game interface
    def interface(self):
            os.system("cls")
            print(f"turn: {self.turn} | {self.human_player.playername}: {self.human_player.score}/{20} | {self.ai.playername}: {self.ai.score}/{20}")
            print(f"{self.human_player.playername}:")
            self.human_player.playerboard.print_board()
            print("__________________________________________________")
            print(f"{self.ai.playername}:")
            self.ai.playerboard.print_board()



    def gameloop(self):
        #flag to break out of nestled loop
        end = False
        while True: 

            #Players turn
            self.turn += 1
            self.interface()
            while True:
                #Expecting input x,y
                try:
                    target_x, target_y = input("Player 1: Choose a coordinate to shoot (x,y)").split(",")
                    target_x = int(target_x)
                    target_y = int(target_y)
                    if self.human_player.check_legal_placement([(target_x, target_y)], placing_ships=False):
                        #checks if player makes a hit and continues turn until player misses
                        if self.human_player.target_shot(target_x-1, target_y-1, opponent=self.ai):
                            #checks if win-condition is met
                            self.interface()
                            if self.check_win(self.human_player):
                                winner = self.human_player.playername
                                print(f"Congratulations! You won!")
                                end = True
                                break
                        else:
                            break
                except Exception as e:
                    print("Incorrect input!")
                    print(e)
            #breaks loop before next turn begins if winner is decided
            if end:
                break

            #AIs turn
            self.interface()
            print("AI: turn in progress..")
            #put a sleep to make it easier to see AIs turn and make it seem like it's "thinking" https://realpython.com/python-sleep/
            time.sleep(3)
            while True:
                #checks if AI makes a hit and continues turn until AI misses
                if self.ai.target_shot(random.randint(0,9), random.randint(0,9), opponent=self.human_player):
                    if self.check_win(self.ai):
                        winner = self.ai.playername
                        self.interface()
                        print(f"You lose! Better luck next time..")
                        end = True
                        break
                else:
                    break
            if end:
                break
        #Saves stats to database /data/game_data.db
        self.stats.save_stats(winner, self.turn)    
        
    #saves players board layout to file that can be used as AIs layout in another game
    def save_board_layout(self):
        print("Would you like to save your board-layout as template? (y/n)")
        while True:
            answer = input("answer: ")
            if answer.lower() == "y":
                self.human_player.save_ship_placement()
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