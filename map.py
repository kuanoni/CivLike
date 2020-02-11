import map_generator
from tile import Tile, ForestTile, WaterTile, HillTile, GroundTile, MountainTile
import random


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.make_map()
        self.populate_map()

    def make_map(self):
        """ Uses map generator to randomly generate a new map. """
        tiles = [[Tile("Empty", "") for y in range(self.height)] for x in range(self.width)]

        map_array = map_generator.make_map(self.width, self.height, 0.47, 10)
        for y in range(self.height):
            for x in range(self.width):
                if map_array[y][x]:
                    tiles[x][y] = GroundTile()
                else:
                    tiles[x][y] = WaterTile()

        return tiles

    def populate_map(self):
        for i in range(5):
            x, y = self.add_hills(MountainTile)
            self.add_hills(MountainTile, x=x, y=y)
        for i in range(15):
            x, y = self.add_hills()
            self.add_hills(x=x, y=y)
        for i in range(20):
            x, y = self.add_hills(ForestTile)
            self.add_hills(ForestTile, x=x, y=y)

    def add_hills(self, tile_to_add=HillTile, x=0, y=0):
        if x == 0 and y == 0:
            x, y = self.get_random_open_tile_pos()
        adj_tiles = self.get_adjacent_tiles_by_pos(x, y)
        keys_to_rem = []
        valid_positions = [(x, y)]
        for k, tile in adj_tiles.items():
            if tile is None or tile.blocked:
                keys_to_rem.append(k)
            else:
                valid_positions.append(k)

        for k in keys_to_rem:
            adj_tiles.pop(k)

        random.shuffle(valid_positions)
        i = int(len(valid_positions)/2)
        valid_positions = valid_positions[i:]

        for pos in valid_positions:
            self.add_tile(tile_to_add(), pos[0], pos[1])

        return valid_positions[-1]

    def render(self, console, offset_x=0, offset_y=0):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[x][y]
                console.print(x, y, tile.char, tile.fg_color, tile.bg_color)

    def get_tile_by_pos(self, x, y):
        """ Returns tile from map position. """
        if x > self.width-1 or y > self.height:
            return None
        try:
            if self.tiles[x][y]:
                return self.tiles[x][y]
        except IndexError:
            raise IndexError(f"No tile exists at X:{x} Y:{y}")

    def get_tile_pos(self, tile):
        """ Returns x and y of a tile. """
        for i, x in enumerate(self.tiles):
            if tile in x:
                return i, x.index(tile)

    def add_tile(self, tile, x, y):
        """ Adds tile to position on the map. """
        if x > self.width or y > self.height:
            return
        self.tiles[x][y] = tile

    def get_adjacent_tiles_by_pos(self, x, y):
        """ Returns a dict of adjacent tiles, with the key as the position, and the value as the tile. """
        adj_tiles = {}
        for _y in range(y-1, y+2):
            for _x in range(x-1, x+2):
                try:
                    adj_tiles[(_x, _y)] = self.tiles[_x][_y]
                except IndexError:
                    adj_tiles[(_x, _y)] = None
        adj_tiles[(x, y)] = None
        return adj_tiles

    def get_random_open_tile_pos(self, tiles=[]):
        """ Returns the position of a random unblocked tile. """
        if len(tiles) < 1:
            tiles = self.tiles
        open_pos = []
        for y in range(self.height):
            for x in range(self.width):
                if not tiles[x][y].blocked:
                    open_pos.append((x, y))
        random.shuffle(open_pos)
        return open_pos[0]