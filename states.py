import tcod.event

from entities import Settler
from gui import GUI


class State:
    def __init__(self, gui_state, event_handler):
        self.gui_state = gui_state
        self.event_handler = event_handler


class BaseState(State):
    def __init__(self, game):
        super().__init__(GUI.render_base, BaseEventHandler(game))
        self.game = game


class InspectTile(State):
    def __init__(self, game, tile):
        super().__init__(GUI.render_inspect_tile, BaseEventHandler(game))
        self.tile = tile


class InspectEntity(State):
    def __init__(self, game, entity, tile):
        super().__init__(GUI.render_inspect_entity, InspectEntityEventHandler(game))
        self.entity = entity
        self.tile = tile
        self.move = False


class MoveEntity(State):
    def __init__(self, game, entity):
        super().__init__(GUI.render_move_entity, MoveEntityEventHandler(game))
        self.entity = entity


class SettleCity(State):
    def __init__(self, game, entity):
        super().__init__(GUI.render_settle_city, SettleCityEventHandler(game))
        self.entity = entity


class Attack(State):
    def __init__(self, game, entity):
        super().__init__(GUI.render_attack, AttackEventHandler(game))
        self.entity = entity


class EventHandler(tcod.event.EventDispatch):
    def __init__(self, game):
        self.game = game

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        pass

    def ev_mousebuttondown(self, event):
        pass

    def ev_mousemotion(self, event):
        pass


class BaseEventHandler(EventHandler):
    """ Event handler for the base game. """

    def __init__(self, game):
        super().__init__(game)

    def ev_keydown(self, event):
        if event.sym == 32:  # spacebar key
            self.game.pass_turn()

    def ev_mousebuttondown(self, event):
        """ 1: Left mouse button
            2: Middle mouse button
            3: Right mouse button """
        if event.button == 1:
            x, y = event.tile.x, event.tile.y
            entity = self.game.get_entity_by_pos(x, y)
            tile = self.game.game_map.get_tile_by_pos(x, y)

            if entity and tile:
                self.game.set_state(InspectEntity(self.game, entity, tile))
                return
            if tile:
                self.game.set_state(InspectTile(self.game, tile))

        elif event.button == 2:
            pass
        elif event.button == 3:
            """ Place a Settler for debugging purposes. """
            x, y = event.tile.x, event.tile.y
            self.game.add_entity(Settler(x, y))


class InspectEntityEventHandler(BaseEventHandler):
    """ Event handler for when an entity has been clicked and is being inspected. """

    def __init__(self, game):
        super().__init__(game)

    def ev_keydown(self, event):
        """ M key: Starts the MoveEntity state.
        N key: Starts the SettleCity state. """
        entity = self.game.state.entity
        if event.sym == 97:  # A key
            self.game.set_state(Attack(self.game, entity))
        if event.sym == 109:  # M key
            self.game.set_state(MoveEntity(self.game, entity))
        if event.sym == 110 and entity.turn_into_tile:  # N key
            self.game.set_state(SettleCity(self.game, entity))

        super().ev_keydown(event)


class MoveEntityEventHandler(EventHandler):
    """ Event handler for when the player decides to move an entity. """

    def __init__(self, game):
        super().__init__(game)
        self.path_cost = 0

    def ev_keydown(self, event):
        """ ESC key: Cancels the MoveEntity state and goes back to InspectEntity. """
        entity = self.game.state.entity
        if event.sym == 27:  # ESC key
            tile = self.game.game_map.get_tile_by_pos(entity.x, entity.y)
            self.game.set_state(InspectEntity(self.game, entity, tile))

    def ev_mousebuttondown(self, event):
        """ Generates a path for the entity to travel to where the mouse was clicked. """
        if event.button == 1:
            x, y = event.tile.x, event.tile.y
            entity = self.game.state.entity
            path = self.game.get_entity_move_path(entity, x, y)
            if len(path) > 0:
                entity.move_path = path
                self.game.set_state(BaseState(self.game))

    def ev_mousemotion(self, event):
        """ Generates a path cost. """
        x, y = event.tile.x, event.tile.y
        entity = self.game.state.entity
        tcod.console_set_char_background(0, x, y, entity.fg_color)
        tcod.console_set_char_foreground(0, x, y, entity.fg_color)


class SettleCityEventHandler(EventHandler):
    """ Event handler for when an entity is settling a city. """

    def __init__(self, game):
        super().__init__(game)
        self.city_name = ""
        self.can_type = False

    def ev_keydown(self, event):
        """ ESC key: Cancels the SettleCity state and goes back to InspectEntity.
        ENTER key: Settles the city. """
        entity = self.game.state.entity
        tile = self.game.game_map.get_tile_by_pos(entity.x, entity.y)
        if event.sym == 27 and entity.turn_into_tile:  # ESC key
            self.game.set_state(InspectEntity(self.game, entity, tile))
        elif event.sym == 13 and len(self.city_name) > 1:  # ENTER key
            self.game.settle_city(self.city_name, entity)
            self.game.set_state(BaseState(self.game))
        elif event.sym == 8:
            self.city_name = self.city_name[:-1]
        else:
            pass

        super().ev_keydown(event)

    def ev_textinput(self, event):
        """ Allows user to type in the city name. """
        if self.can_type:
            self.city_name += event.text
        else:
            """ The 'N' press required to enter this state causes an 'N' to
            immediately entered into this text input. This statement is required 
            to prevent the city name from starting with 'N'. """
            self.city_name = ""
            self.can_type = True
            return


class AttackEventHandler(EventHandler):
    """ Event handler for when an entity is settling a city. """

    def __init__(self, game):
        super().__init__(game)

    def ev_keydown(self, event):
        """ ESC key: Cancels the Attack state and goes back to InspectEntity. """
        entity = self.game.state.entity
        tile = self.game.game_map.get_tile_by_pos(entity.x, entity.y)
        if event.sym == 27:  # ESC key
            self.game.set_state(InspectEntity(self.game, entity, tile))

    def ev_mousebuttondown(self, event):
        """ Attempts to attack a target within range. """
        if event.button == 1:
            x, y = event.tile.x, event.tile.y
            entity = self.game.state.entity
            success = self.game.set_entity_attack(entity, x, y)
            if success:
                tile = self.game.game_map.get_tile_by_pos(entity.x, entity.y)
                self.game.set_state(InspectEntity(self.game, entity, tile))
