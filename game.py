import tcod, tcod.path, tcod.map

from entities import Settler, Warrior
from gui import GUI
from map import Map
from states import BaseState, State
from tile import CityTile
import random


class Game:
    def __init__(self, root_console):
        self.gui = GUI(root_console)
        self.game_console = tcod.console.Console(40, 40)
        self.state = BaseState(self)

        self.game_map = Map(self.game_console.width, self.game_console.height)
        self.teams = ["RED_TEAM", "BLUE_TEAM"]
        self.team_entities = {}
        for team in self.teams:
            self.team_entities[team] = []
        self.place_team("RED_TEAM")
        self.place_team("BLUE_TEAM")

        self.turn = 0

    def set_state(self, state):
        """ Sets the game state. """
        self.state = state

    def add_entity(self, team, entity):
        """ Adds entity. """
        if team and entity:
            self.team_entities[team].append(entity)

    def remove_entity(self, entity):
        """ Removes entity. """
        entity_to_remove = None
        for team in self.team_entities.keys():
            for _entity in self.team_entities[team]:
                if _entity is entity:
                    i = self.team_entities[team].index(_entity)
                    self.team_entities[team].pop(i)
                    break

    def get_entity_by_pos(self, x, y):
        """ Get an entity by it's x and y coordinates. """
        for team in self.team_entities.keys():
            for entity in self.team_entities[team]:
                if entity.x == x and entity.y == y:
                    return entity
        return None

    def get_entity_path_cost(self, entity, path=None):
        if path is None:
            path = entity.move_path
        move_costs = []
        if len(entity.move_path) > 0:
            for pos in path:
                move_costs.append(self.game_map.get_tile_by_pos(pos[0], pos[1]).move_penalty)

        return move_costs

    def move_entity(self, entity):
        """ Moves an entity using it's move_path, which is generated from A* pathfinding. """
        if len(entity.move_path) > 0:
            move_costs = self.get_entity_path_cost(entity)

            move_to = (0, 0)
            move_points = float(entity.movement)

            for i, cost in enumerate(move_costs):
                if cost > move_points:
                    break
                move_to = entity.move_path[i]
                move_points -= cost

            entity.x, entity.y = move_to
            index = entity.move_path.index(move_to)
            entity.move_path = entity.move_path[index+1:]

    def get_entity_move_path(self, entity, dest_x, dest_y):
        """ Generate an A* path for an entity, to a destination. """
        blocked_map = tcod.map.Map(self.game_map.width, self.game_map.height)
        for y in range(self.game_map.width):
            for x in range(self.game_map.height):
                blocked_map.walkable[y][x] = not self._is_pos_blocked(x, y)

        astar = tcod.path.AStar(blocked_map, diagonal=0)
        path = astar.get_path(entity.x, entity.y, dest_x, dest_y)
        return path

    def set_entity_attack(self, entity, x, y):
        """ Entity attempts to attack the target at (x, y). """
        target = self.get_entity_by_pos(x, y)
        if not target:
            return False
        if target.team == entity.team:
            return False
        if target.x in range(entity.x - entity.atk_range, entity.x + entity.atk_range + 1) and \
                target.y in range(entity.y - entity.atk_range, entity.y + entity.atk_range + 1):
            """ Damage calculations
                TODO:
                - Include terrain defense bonuses
                - Include health based damage
            """
            target.hp -= int(entity.atk * (1 - self.game_map.get_tile_by_pos(entity.x, entity.y).defense_bonus))
            entity.hp -= target.atk
            return True

    def place_team(self, team):
        pos = self.game_map.get_random_open_tile_pos()
        adj_tiles = self.game_map.get_adjacent_tiles_by_pos(pos[0], pos[1])
        keys_to_rem = []
        valid_keys = []
        for k, tile in adj_tiles.items():
            if tile is None or tile.blocked:
                keys_to_rem.append(k)
            else:
                valid_keys.append(k)

        for k in keys_to_rem:
            adj_tiles.pop(k)
        random.shuffle(valid_keys)
        war_x, war_y = valid_keys[0]
        self.add_entity(team, Settler(team, pos[0], pos[1]))
        self.add_entity(team, Warrior(team, war_x, war_y))

    def pass_turn(self):
        """ Pass a game turn. """
        for team in self.teams:
            for entity in self.team_entities[team]:
                self.move_entity(entity)
        self.turn += 1
        self.state = BaseState(self)

    def settle_city(self, name, entity):
        """ Turn an entity into a city. """
        adj_tiles = self.game_map.get_adjacent_tiles_by_pos(entity.x, entity.y)
        city = CityTile(name, entity.team)
        for tile in adj_tiles.values():
            if tile:
                city.production_bonus += tile.production_bonus
                city.food_bonus += tile.food_bonus

        self.game_map.add_tile(city, entity.x, entity.y)
        self.remove_entity(entity)

    def _is_pos_blocked(self, x, y):
        """ Is position blocked by impassable terrain or an entity? """
        is_entity = self.get_entity_by_pos(x, y)
        if is_entity:
            is_entity = True
        return self.game_map.tiles[x][y].blocked or is_entity

    def render(self, root_console):
        """ Render to root console. """
        self.game_map.render(self.game_console)
        for team, entities in self.team_entities.items():
            for entity in entities:
                self.game_console.print(entity.x, entity.y, entity.char, entity.fg_color)
        self.game_console.blit(root_console, 0, 0, 0, 0, self.game_console.width, self.game_console.height)
        self.gui.render(self.state)
