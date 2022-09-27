class ship:
    def __init__(self, length, rotation, start_x, start_y):
        self.rotation = rotation
        self.length = length
        self.start_x = start_x
        self.start_y = start_y
    
    def get_coordinates(self):
        coordinates = []
        coordinates.append((self.start_x, self.start_y))
        if self.rotation == 'r':
            for x in range(self.length):
                coordinates.append((self.start_x+x, self.start_y))
        return coordinates


class player:
    pass

class human(player):
    pass

class AI(player):
    pass
