from constants import colors, team_colors

class Tile:
    def __init__(self, name, char, fg_color=(255, 255, 255), bg_color=(0, 0, 0), blocked=False):
        self.name = name
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.blocked = blocked


class WaterTile(Tile):
    def __init__(self):
        super().__init__("Water", "░", fg_color=colors["water_fg"], bg_color=colors["water_bg"], blocked=True)
        self.move_penalty = 100
        self.defense_bonus = 0


class GroundTile(Tile):
    def __init__(self):
        super().__init__("Ground", "▓", fg_color=(153, 61, 0), bg_color=colors["ground"])
        self.move_penalty = 1
        self.defense_bonus = 0


class ForestTile(Tile):
    def __init__(self):
        super().__init__("Forest", "♣", fg_color=colors["forest"], bg_color=colors["ground"])
        self.move_penalty = 1.5
        self.defense_bonus = 0.2

class HillTile(Tile):
    def __init__(self):
        super().__init__("Hill", "◊", fg_color=colors["hill"], bg_color=colors["ground"])
        self.move_penalty = 1.5
        self.defense_bonus = 0.3

class MountainTile(Tile):
    def __init__(self):
        super().__init__("Mountain", "▲", fg_color=colors["mountain"], bg_color=colors["ground"], blocked=True)
        self.move_penalty = 100
        self.defense_bonus = 0

class CityTile(Tile):
    def __init__(self, name, team):
        super().__init__(name, "Ω", fg_color=team_colors[team], bg_color=colors["ground"])
        self.team = team
        self.move_penalty = 1
        self.defense_bonus = 0
