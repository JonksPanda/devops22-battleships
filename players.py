class ship:
    def __init__(self, length, rotation, start_x, start_y):
        self.rotation = rotation.lower()
        self.length = length
        self.start_x = start_x
        self.start_y = start_y
    
    def get_coordinates(self):
        coordinates = []
        if self.rotation == 'right':
            for x in range(self.length):
                coordinates.append((int(self.start_x)+x, int(self.start_y)))
        elif self.rotation == 'left':
            for x in range(self.length):
                coordinates.append((int(self.start_x)-x, int(self.start_y)))
        elif self.rotation == 'up':
            for y in range(self.length):
                coordinates.append((int(self.start_x), int(self.start_y)+y))
        elif self.rotation == 'down':
            for y in range(self.length):
                coordinates.append((int(self.start_x), int(self.start_y)-y))
        return coordinates


class player:
    pass

class human(player):
    pass

class AI(player):
    pass
