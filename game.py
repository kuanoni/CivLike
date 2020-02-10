import tcod
import tcod.path

from gui import GUI
from map import Map
from states import BaseState, State
from tile import CityTile


class Game:
    def __init__(self, root_console):
        self.gui = GUI(root_console)
        self.game_console = tcod.console.Console(40, 40)
        self.state = BaseState(self)

        self.game_map = Map(self.game_console.width, self.game_console.height)
        self.entities = []

        self.turn = 0

    def set_state(self, state):
        """ Sets the game state. """
        self.state = state

    def add_entity(self, entity):
        """ Adds entity. """
        if entity:
            self.entities.append(entity)

    def remove_entity(self, entity):
        """ Removes entity. """
        i_remove = self.entities.index(entity)
        self.entities.pop(i_remove)

    def get_entity_by_pos(self, x, y):
        """ Get an entity by it's x and y coordinates. """
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return False

    def move_entity(self, entity):
        """ Moves an entity using it's move_path, which is generated from A* pathfinding. """
        if len(entity.move_path) > 0:
            pos = entity.move_path.pop(0)
            entity.x, entity.y = pos

    def get_entity_move_path(self, entity, dest_x, dest_y):
        """ Generate an A* path for an entity, to a destination. """
        blocked_map = tcod.map_new(self.game_map.width, self.game_map.height)
        for y in range(self.game_map.width):
            for x in range(self.game_map.height):
                tcod.map_set_properties(blocked_map, x, y, True, not self._is_pos_blocked(x, y))

        astar = tcod.path.AStar(blocked_map, diagonal=0)
        path = astar.get_path(entity.x, entity.y, dest_x, dest_y)
        return path

    def pass_turn(self):
        """ Pass a game turn. """
        for entity in self.entities:
            self.move_entity(entity)
        self.turn += 1
        self.state = BaseState(self)

    def settle_city(self, name, entity):
        """ Turn an entity into a city. """
        self.game_map.add_tile(CityTile(name[1:]), entity.x, entity.y)
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
        for entity in self.entities:
            self.game_console.print(entity.x, entity.y, entity.char, entity.fg_color)
        self.game_console.blit(root_console, 0, 0, 0, 0, self.game_console.width, self.game_console.height)
        self.gui.render(self.state)
