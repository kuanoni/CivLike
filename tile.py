from constants import colors, team_colors


class Tile:
    def __init__(self, name, char, fg_color=(255, 255, 255), bg_color=(0, 0, 0), blocked=False):
        self.name = name
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.blocked = blocked

        self.move_penalty = 100
        self.defense_bonus = 0

        self.production_bonus = 0
        self.food_bonus = 0


class BlockedTile(Tile):
    def __init__(self, name, char, fg_color=(255, 255, 255), bg_color=(0, 0, 0)):
        super().__init__(name, char, fg_color, bg_color, True)

class WaterTile(BlockedTile):
    def __init__(self):
        super().__init__("Water", "░", fg_color=colors["water_fg"], bg_color=colors["water_bg"])
        self.food_bonus = 2


class GroundTile(Tile):
    def __init__(self):
        super().__init__("Ground", "▓", fg_color=(153, 61, 0), bg_color=colors["ground"])
        self.move_penalty = 1
        self.defense_bonus = 0
        self.production_bonus = 1
        self.food_bonus = 1


class ForestTile(Tile):
    def __init__(self):
        super().__init__("Forest", "♣", fg_color=colors["forest"], bg_color=colors["ground"])
        self.move_penalty = 1.5
        self.defense_bonus = 0.2
        self.production_bonus = 2
        self.food_bonus = 1


class HillTile(Tile):
    def __init__(self):
        super().__init__("Hill", "◊", fg_color=colors["hill"], bg_color=colors["ground"])
        self.move_penalty = 1.5
        self.defense_bonus = 0.3
        self.production_bonus = 3


class MountainTile(BlockedTile):
    def __init__(self):
        super().__init__("Mountain", "▲", fg_color=colors["mountain"], bg_color=colors["ground"])
        self.production_bonus = 3


class CityTile(Tile):
    def __init__(self, name, team):
        super().__init__(name, "Ω", fg_color=team_colors[team], bg_color=colors["ground"])
        self.team = team
        self.move_penalty = 1
