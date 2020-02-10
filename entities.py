from tile import CityTile


class Entity:
    def __init__(self, name, char, x, y, fg_color=(255, 255, 255)):
        self.name = name
        self.char = char
        self.x = x
        self.y = y
        self.fg_color = fg_color

        self.move_path = []

        self.turn_into_tile = False


class Settler(Entity):
    def __init__(self, x, y):
        super().__init__("Settler", "☻", x, y)
        self.turn_into_tile = True


class Warrior(Entity):
    def __init__(self, x, y):
        super().__init__("Warrior", "☺", x, y)