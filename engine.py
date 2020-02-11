import tcod
import tcod.event
import tcod.console

from event_handlers import EventHandler
from game import Game

class Engine:
    def __init__(self):
        self.SCREEN_WIDTH = 60
        self.SCREEN_HEIGHT = 40
        self.FONT = "resources/fonts/terminal16x16_gs_ro.png"

        tcod.console_set_custom_font(self.FONT, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_ASCII_INROW)
        self.root_console = tcod.console_init_root(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "CivLike", False, tcod.RENDERER_SDL2, order="F", vsync=False
        )

        self.game = Game(self.root_console)
        self.event_handler = EventHandler(self.game)

        self._map_fonts()

    def game_loop(self):
        while tcod.event.Quit():
            tcod.console_flush()
            self.root_console.clear(fg=(255, 255, 255), bg=(0, 0, 0))
            self.game.render(self.root_console)

            for event in tcod.event.wait():
                self.game.state.event_handler.dispatch(event)
                # self.event_handler.dispatch(event)

    def _map_fonts(self):
        """ Map ASCII characters to the font map. """
        tcod.console_map_string_to_font("☻", 1, 0)
        tcod.console_map_string_to_font("☺", 2, 0)
        tcod.console_map_string_to_font("♣", 5, 0)
        tcod.console_map_string_to_font("░", 2, 11)
        tcod.console_map_string_to_font("▓", 1, 11)
        tcod.console_map_string_to_font("Ω", 10, 14)
        tcod.console_map_string_to_font("▲", 14, 1)
        tcod.console_map_string_to_font("◊", 4, 0)


if __name__ == '__main__':
    engine = Engine()
    engine.game_loop()
