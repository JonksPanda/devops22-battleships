import os
import game
import stats
import time

class menu:
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__)) #https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
        #Reads title
        #https://www.pythontutorial.net/python-basics/python-read-text-file/
        with open(f"{path}/other/splash-text.txt") as file:
            self.splash = file.read()

    def main_menu(self):


        menu_options = """
1. start/load game
2. load stats
3. quit
        """
        print(menu_options)
        choice = input("option: ")

        if choice == "1":
            print("starting game.. ")
            time.sleep(1)
            os.system("cls")
            game.main()
        elif choice == "2":
            print("loading stats..")
            time.sleep(1)
            os.system("cls")
            stats.main()
        elif choice == "3":
            print("quitting game.. ")
            time.sleep(1)
            quit()
        else:
            os.system("cls")
            self.menu_loop()

    def game_menu(self):
        print("Hello World!")

    def stats_menu(self):
        pass

    def options_menu(self):
        pass

    def menu_loop(self):
        while True:
            print(self.splash)
            self.main_menu()

def main():
    os.system("cls")
    menu().menu_loop()

if __name__ == "__main__":
    main()