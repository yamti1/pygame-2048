from pyprocessing import *
import numpy as np
import random

BOARD_SIZE = 4, 4  # num_rows, num_columns
PROB_SPAWN_2 = .75  # the probability to spawn a '2' tile instead of a '4' tile

board = np.zeros(BOARD_SIZE, int)


def merge_tiles(tiles):
    i = 0
    while i < len(tiles) - 2:
        if tiles[i] == tiles[i+1]:
            tiles[i] += tiles[i+1]
            del tiles[i+1]
            continue
        i += 1

    return tiles  # for convenience. the tiles are merged in-place.


def spawn_tile():
    """
    Spawns a new tile in a clear spot on the board.
    The tile can be a '2' tile or a '4' tile, randomly according to PROB_SPAWN_2.
    :return: The number of clear spots on the board after spawning.
    """
    clear_tiles = []
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == 0:
                clear_tiles.append((i, j))

    if clear_tiles:
        board[random.choice(clear_tiles)] = 2 if random.random() < PROB_SPAWN_2 else 4

    return len(clear_tiles) - 1


def is_game_over():
    pass


def game_over():
    pass


def keyPressed():
    if key.char != CODED:
        return

    if key.code == UP:
        for i in range(BOARD_SIZE[1]):
            column = merge_tiles(list(board[:, i]))
            column += [0] * (BOARD_SIZE[0] - len(column))
            board[:, i] = column

    elif key.code == DOWN:
        for i in range(BOARD_SIZE[1]):
            reversed_column = merge_tiles(list(reversed(board[:, i])))
            reversed_column += [0] * (BOARD_SIZE[0] - len(reversed_column))
            board[:, i] = reversed(reversed_column)

    elif key.code == LEFT:
        for i in range(BOARD_SIZE[0]):
            row = merge_tiles(list(board[i, :]))
            row += [0] * (BOARD_SIZE[1] - len(row))
            board[i, :] = row

    elif key.code == RIGHT:
        for i in range(BOARD_SIZE[0]):
            reversed_row = merge_tiles(list(reversed(board[i, :])))
            reversed_row += [0] * (BOARD_SIZE[1] - len(reversed_row))
            board[i, :] = reversed(reversed_row)

    spawn_tile()

    if is_game_over():
        game_over()


def setup():
    pass


def draw():
    pass

run()
