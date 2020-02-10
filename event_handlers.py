import tcod.event

from entities import Settler
from states import InspectTile, InspectEntity
from tile import Tile, CityTile


class EventHandler(tcod.event.EventDispatch):
    def __init__(self, game):
        self.game = game

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        print(event)

    def ev_mousebuttondown(self, event):
        """ 1: Left mouse button
            2: Middle mouse button
            3: Right mouse button """
        if event.button == 1:
            x, y = event.tile.x, event.tile.y
            entity = self.game.get_entity_by_pos(x, y)
            tile = self.game.game_map.get_tile(x, y)

            if entity and tile:
                self.game.set_state(InspectEntity(entity, tile))
                return
            if tile:
                self.game.set_state(InspectTile(tile))

        elif event.button == 2:
            pass
        elif event.button == 3:
            x, y = event.tile.x, event.tile.y
            self.game.add_entity(Settler(x, y))

    def ev_mousemotion(self, event):
        pass
