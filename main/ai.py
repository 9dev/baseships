import json
from random import randint

from main.models import BOARD_SIZE, State


def ai_move(game):
    player_board = json.loads(game.player_board)
    state = State.MISSED

    while state == State.MISSED or state == State.HIT:
        x, y = randint(0, BOARD_SIZE-1), randint(0, BOARD_SIZE-1)
        state = int(player_board[x][y])

    if state == State.EMPTY:
        state = State.MISSED
        game.update_player_board(x, y, state)
    elif state == State.FILLED:
        state = State.HIT
        game.update_player_board(x, y, state)

    return {'x': x, 'y': y, 'state': state}


def ai_moves(game):
    moves = []

    while True:
        move = ai_move(game)
        moves.append(move)

        if move['state'] == State.MISSED:
            break

    return moves
