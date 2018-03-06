from pyprocessing import *
import numpy as np

BOARD_SIZE = 4, 4  # num_rows, num_columns

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



def setup():
    pass


def draw():
    pass

run()
