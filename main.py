"""runs the project."""

import os
import menu


def main():
    """Inits the project."""
    #Checks if neccesary paths exists before starting the game
    data = f"{os.path.dirname(os.path.realpath(__file__))}/data"
    fleets = f"{os.path.dirname(os.path.realpath(__file__))}/data/fleets"
    if os.path.exists(data) is False:
        os.makedirs(data)
    if os.path.exists(fleets) is False:
        os.makedirs(fleets)
    menu.main()

if __name__ == "__main__":
    main()
    