from pyprocessing import *
import numpy as np
import random
from contextlib import suppress

# region Constants
# Gameplay Constants
BOARD_SIZE = 4, 4  # num_rows, num_columns
PROB_SPAWN_2 = .75  # the probability to spawn a '2' tile instead of a '4' tile
TARGET_TILE = 2048

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
game_is_over = False


def merge_tiles(tiles):
    tiles = [tile for tile in tiles if tile != 0]  # remove all zero-tiles
    i = 0
    while i < len(tiles) - 1:
        if tiles[i] == tiles[i+1]:
            tiles[i] += tiles[i+1]
            del tiles[i+1]
        if tiles[i] == TARGET_TILE:
            game_over()
            break
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
            neighbours = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

            # remove neighbours with negative indexes
            neighbours = [(row, col) for row, col in neighbours if row > -1 and col > -1]

            for neighbour in neighbours:
                with suppress(IndexError):
                    if tile == board[neighbour]:
                        return False
    return True


def game_over():
    global game_is_over
    game_is_over = True
    textAlign(CENTER, CENTER)
    textSize(50)
    fill(0)
    text("Game Over", width/2, height - BOTTOM_EDGE/2)


def update_board(dimension, reverse=False):
    other_dimension = -dimension + 1  # 0 => 1; 1 => 0
    for i in range(BOARD_SIZE[dimension]):
        target_indexes = (..., i) if dimension == 1 else (i, ...)

        tiles = board[target_indexes]                               # get the tiles from the board
        tiles = list(reversed(tiles) if reverse else tiles)         # reverse the tiles if needed
        tiles = merge_tiles(tiles)                                  # merge the tiles
        tiles += [0] * (BOARD_SIZE[other_dimension] - len(tiles))   # add zero tiles to complete the row/column
        tiles = list(reversed(tiles) if reverse else tiles)         # re-reverse the tiles if needed

        board[target_indexes] = tiles                               # set the updated tiles to the board


def keyPressed():
    if key.char != CODED:
        return
    if game_is_over:
        return

    map_keycode_to_args = {
        UP: [0],
        DOWN: [0, True],
        LEFT: [1],
        RIGHT: [1, True],
    }
    with suppress(KeyError):
        update_board(*map_keycode_to_args[key.code])

    num_clear_tiles = spawn_tile()

    update_frame()

    if is_game_over(num_clear_tiles):
        game_over()


def update_frame():
    background(BACKGROUND_COLOR)

    # Board railing
    fill(RAILING_COLOR)
    noStroke()
    rect(SIDE_EDGES, TOP_EDGE, width - SIDE_EDGES * 2, height - TOP_EDGE - BOTTOM_EDGE)

    # Board tiles
    noStroke()
    for i in range(BOARD_SIZE[0]):
        for j in range(BOARD_SIZE[1]):
            tile = board[i, j]

            fill(EMPTY_TILE_COLOR if tile == 0 else 255)
            x = SIDE_EDGES + BOARD_RAILING + (BOARD_RAILING + TILE_WIDTH) * i
            y = TOP_EDGE + BOARD_RAILING + (BOARD_RAILING + TILE_HEIGHT) * j
            rect(x, y, TILE_WIDTH, TILE_HEIGHT)

            if tile == 0:
                continue  # don't write '0' in a zero tile

            fill(0)
            textAlign(CENTER, CENTER)
            text(str(board[i, j]), x + TILE_WIDTH/2, y + TILE_HEIGHT/2)


def main():
    w = SIDE_EDGES * 2 + (TILE_WIDTH + BOARD_RAILING) * BOARD_SIZE[0] + BOARD_RAILING
    h = TOP_EDGE + BOTTOM_EDGE + (TILE_HEIGHT + BOARD_RAILING) * BOARD_SIZE[1] + BOARD_RAILING
    size(w, h, caption='2048')

    update_frame()

    noLoop()
    run()

if __name__ == '__main__':
    main()
