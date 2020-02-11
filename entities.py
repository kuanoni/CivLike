from constants import team_colors

class Entity:
    def __init__(self, name, char, team, x, y):
        self.name = name
        self.char = char
        self.team = team
        self.x = x
        self.y = y
        self.fg_color = team_colors[team]

        self.move_path = []

        self.turn_into_tile = False

class EntityStats:
    def __init__(self, max_hp, atk, movement):
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.movement = movement

class Settler(Entity, EntityStats):
    def __init__(self, team, x, y):
        super().__init__("Settler", "S", team, x, y)
        self.turn_into_tile = True
        self.max_hp = 10
        self.hp = 10
        self.atk = 0
        self.atk_range = 0
        self.movement = 3.5


class Warrior(Entity):
    def __init__(self, team, x, y):
        super().__init__("Warrior", "W", team, x, y)
        self.max_hp = 30
        self.hp = 30
        self.atk = 12
        self.atk_range = 1
        self.movement = 2.5
