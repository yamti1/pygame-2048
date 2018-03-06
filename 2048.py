from pyprocessing import *
import numpy as np
import random
from contextlib import suppress

# region Constants
# Gameplay Constants
BOARD_SIZE = 4, 4  # num_rows, num_columns
PROB_SPAWN_2 = .75  # the probability to spawn a '2' tile instead of a '4' tile

# Graphics Constants
BOARD_RAILING = 10
TILE_WIDTH = 90
TILE_HEIGHT = 90
SIDE_EDGES = 70
TOP_EDGE = 30
BOTTOM_EDGE = 100
BACKGROUND_COLOR = 230
RAILING_COLOR = 150
EMPTY_TILE_COLOR = 170
# endregion

board = np.zeros(BOARD_SIZE, int)


def merge_tiles(tiles):
    # TODO: delete all '0' tiles here, to move all of the tiles to the beginning of the list.
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


def is_game_over(num_clear_tiles):
    if num_clear_tiles > 0:
        return False

    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            neighbours = (i+1, j), (i, j+1), (i-1, j), (i, j-1)
            for neighbour in neighbours:
                with suppress(IndexError):
                    if tile == board[neighbour]:
                        return False
    return True


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

    num_clear_tiles = spawn_tile()

    if is_game_over(num_clear_tiles):
        game_over()

    loop()  # render a single frame (noLoop() is called at the end of draw())


def setup():
    w = SIDE_EDGES * 2 + (TILE_WIDTH + BOARD_RAILING) * BOARD_SIZE[0] + BOARD_RAILING
    h = TOP_EDGE + BOTTOM_EDGE + (TILE_HEIGHT + BOARD_RAILING) * BOARD_SIZE[1] + BOARD_RAILING
    size(w, h, caption='2048')


def draw():
    background(BACKGROUND_COLOR)

    # Board railing
    fill(RAILING_COLOR)
    noStroke()
    rect(SIDE_EDGES, TOP_EDGE, width - SIDE_EDGES * 2, height - TOP_EDGE - BOTTOM_EDGE)

    # Board tiles
    noStroke()
    for i in range(BOARD_SIZE[0]):
        for j in range(BOARD_SIZE[1]):
            x = SIDE_EDGES + BOARD_RAILING + (BOARD_RAILING + TILE_WIDTH) * i
            y = TOP_EDGE + BOARD_RAILING + (BOARD_RAILING + TILE_HEIGHT) * j
            if board[i, j] == 0:
                fill(EMPTY_TILE_COLOR)
            else:
                fill(255)
            rect(x, y, TILE_WIDTH, TILE_HEIGHT)

    noLoop()  # another frame will be rendered on keyPressed()

run()
