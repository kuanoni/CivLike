import tcod.console


class GUI:
    def __init__(self, root_console):
        self.root_console = root_console
        self.width = 20
        self.height = root_console.height
        self.console = tcod.console.Console(self.width, self.height)

    def render_base(self, state):
        turn = str(state.game.turn)
        self.console.print(1, 1, "Turn: ")
        self.console.print(7, 1, turn)

    def render_inspect_tile(self, state):
        """ Render the inspect tile state gui. """
        tile = state.tile
        self.console.print(1, 1, tile.name)
        self.console.hline(1, 2, self.width - 2)

    def render_inspect_entity(self, state):
        """ Render the inspect entity state gui. """
        entity = state.entity
        tile = state.tile

        self.console.print(1, 1, entity.name, entity.fg_color)
        self.console.hline(1, 2, self.width - 2)
        self.console.print(1, 3, "Standing on " + tile.name)
        self.console.hline(1, 4, self.width - 2)
        self.console.print(1, 38, "M:", (0, 255, 0))
        self.console.print(4, 38, "Move entity")
        if entity.turn_into_tile:
            self.console.print(1, 37, "N:", (0, 255, 0))
            self.console.print(4, 37, "Settle city")

    def render_move_entity(self, state):
        entity = state.entity
        self.console.print(1, 1, entity.name, entity.fg_color)
        self.console.hline(1, 2, self.width - 2)
        self.console.print(1, 3, "Move Cost:")
        self.console.print(12, 3, str(state.event_handler.path_len))
        self.console.print(1, 38, "M:", (0, 255, 0))
        self.console.print(3, 38, "Cancel move")

    def render_settle_city(self, state):
        entity = state.entity
        self.console.print(1, 1, "Enter city name:")
        self.console.print(1, 3, state.event_handler.city_name[1:])
        self.console.hline(1, 4, self.width - 2)

        self.console.print(1, 38, "ESC:", (0, 255, 0))
        self.console.print(5, 38, "Cancel settle")

    def render(self, state):
        """ Render the GUI sidebar. """
        self.console.draw_frame(0, 0, self.width, self.height)

        if state.gui_state:
            state.gui_state(self, state)

        self.console.blit(self.root_console, self.root_console.width - self.width, 0, 0, 0, self.width, self.height)