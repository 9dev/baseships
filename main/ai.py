import json
from random import randint

from main.models import BOARD_SIZE, SHIPS, State


def ai_move(game):
    player_board = json.loads(game.player_board)
    state = State.MISSED
    sunk = []

    while state == State.MISSED or state == State.HIT or state == State.SUNK:
        x, y = randint(0, BOARD_SIZE-1), randint(0, BOARD_SIZE-1)
        state = int(player_board[x][y])

    if state == State.EMPTY:
        state = State.MISSED
        game.update_player_board(x, y, state)
    elif state == State.FILLED:
        state, sunk = game.hit_player_ship(x, y)

    return {'x': x, 'y': y, 'state': state}, sunk


def ai_moves(game):
    moves, sunk = [], []

    while True:
        if game.game_over():
            break

        move, sunk_ = ai_move(game)
        moves.append(move)
        sunk += sunk_

        if move['state'] == State.MISSED:
            break

    return moves, sunk


def is_empty(board, x, y):
    if x < 0 or y < 0:
        return False

    try:
        result = int(board[x][y]) == State.EMPTY
        return result
    except IndexError:
        return False


def build_ship(board, x, y, n, dx, dy):
    ship = []

    for k in range(n):
        xx = k * dx + x
        yy = k * dy + y

        if is_empty(board, xx, yy):
            ship.append([xx, yy])
        else:
            return False

    return ship


def place_ship(board, n):
    neighbours = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while True:
        x, y = randint(0, BOARD_SIZE-1), randint(0, BOARD_SIZE-1)

        if is_empty(board, x, y):
            for dx, dy in neighbours:
                ship = build_ship(board, x, y, n, dx, dy)
                if ship:
                    for xx, yy in ship:
                        board[xx] = board[xx][:yy-1] + str(State.FILLED) + board[xx][yy:]
                    return ship


def ai_init():
    board = [str(State.EMPTY) * BOARD_SIZE] * BOARD_SIZE
    ships = []

    for ship in SHIPS:
        ships.append(place_ship(board, ship))

    return json.dumps(board), json.dumps(ships)
