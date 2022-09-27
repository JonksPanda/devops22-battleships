import players
import board

class gamecontrol:
    playerboard = board.board()
    def place_ships(self):
        ship_size = 4
        ship_start_location = input(f"Place ship with {ship_size} blocks (x, y, e.g right)")
        ship_x, ship_y, ship_rotation = ship_start_location.split(", ")

        ship = players.ship(ship_size, ship_rotation, int(ship_x), int(ship_y))
        self.playerboard.players_ships.append(ship.get_coordinates())
        self.playerboard.populate_board()
        self.playerboard.print_board()

    def gameloop(self):
        pass

if __name__ == "__main__":
    game = gamecontrol()
    game.place_ships()