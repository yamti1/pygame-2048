from pyprocessing import *

BOARD_SIZE = 4, 4

board = [[0] * BOARD_SIZE[0]] * BOARD_SIZE[1]


def merge_tiles(tiles):
    i = 0
    while i < len(tiles) - 2:
        if tiles[i] == tiles[i+1]:
            tiles[i] += tiles[i+1]
            del tiles[i+1]
            continue
        i += 1


def setup():
    pass


def draw():
    pass

run()
