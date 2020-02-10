import map_generator
from tile import Tile, ForestTile, WaterTile


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.make_map()

    def make_map(self):
        """ Uses map generator to randomly generate a new map. """
        tiles = [[Tile("Empty", "") for y in range(self.height)] for x in range(self.width)]

        map_array = map_generator.make_map(self.width, self.height, 0.47, 10)
        for y in range(self.height):
            for x in range(self.width):
                if map_array[y][x]:
                    tiles[x][y] = ForestTile()
                else:
                    tiles[x][y] = WaterTile()
        return tiles

    def render(self, console, offset_x=0, offset_y=0):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[x][y]
                console.print(x, y, tile.char, tile.fg_color, tile.bg_color)

    def get_tile(self, x, y):
        """ Returns tile from map position. """
        if x > self.width-1 or y > self.height:
            return None

        try:
            if self.tiles[x][y]:
                return self.tiles[x][y]
        except IndexError:
            raise IndexError(f"No tile exists at X:{x} Y:{y}")

    def add_tile(self, tile, x, y):
        """ Adds tile to position on the map. """
        if x > self.width or y > self.height:
            return
        self.tiles[x][y] = tile