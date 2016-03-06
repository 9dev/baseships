import json
from random import randint

from main.models import BOARD_SIZE, State


def ai_move(game):
    player_board = json.loads(game.player_board)
    state = State.MISSED
    sunk = []

    while state == State.MISSED or state == State.HIT:
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
        move, sunk_ = ai_move(game)
        moves.append(move)
        sunk += sunk_

        if move['state'] == State.MISSED:
            break

    return moves, sunk
