import inspect

class Tile:
    def __init__(self, name, char, fg_color=(255, 255, 255), bg_color=(0, 0, 0), blocked=False):
        self.name = name
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.blocked = blocked

    def __repr__(self):
        return inspect.cleandoc(f"""
        Name: {self.name}
        Character: {self.char}
        """)


class WaterTile(Tile):
    def __init__(self):
        super().__init__("Water", "░", fg_color=(0, 0, 255), bg_color=(0, 215, 255), blocked=True)


class ForestTile(Tile):
    def __init__(self):
        super().__init__("Forest", "♣", fg_color=(76, 255, 0), bg_color=(81, 32, 0))


class CityTile(Tile):
    def __init__(self, name):
        super().__init__(name, "Ω", fg_color=(72, 0, 255), bg_color=(81, 32, 0))

