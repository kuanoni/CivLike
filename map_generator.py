import scipy.signal
import numpy as np


def convolve(tiles: np.array, wall_rule: int = 5) -> np.array:
    neighbors = scipy.signal.convolve2d(
        ~tiles, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "same"
    )
    return neighbors < wall_rule  # Apply the wall rule.


def make_map(width, height, init_chance, convolve_steps):
    # 0: wall, 1: floor
    tiles = np.random.random((height, width)) > init_chance
    for _ in range(convolve_steps):
        tiles = convolve(tiles)
        tiles[[0, -1], :] = 0
        tiles[:, [0, -1]] = 0
    return tiles
