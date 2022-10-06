import menu
import os

def main():
    #Checks if neccesary paths exists before starting the game
    data = f"{os.path.dirname(os.path.realpath(__file__))}/data"
    fleets = f"{os.path.dirname(os.path.realpath(__file__))}/data/fleets"
    if os.path.exists(data) == False:
        os.makedirs(data)
    if os.path.exists(fleets) == False:
        os.makedirs(fleets)
    menu.main()


if __name__ == "__main__":
    main()
