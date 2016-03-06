import json

from django.core.urlresolvers import reverse
from django.db import models


BOARD_SIZE = 10
FIELDS_LENGTH = len(json.dumps([[0] * BOARD_SIZE] * BOARD_SIZE))
SHIPS = [5, 4, 3, 2, 2, 1, 1]


class State(object):
    EMPTY = 0
    FILLED = 1
    MISSED = 2
    HIT = 3
    SUNK = 4


class Game(models.Model):
    player_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
    ai_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)

    player_ships = models.CharField(max_length=FIELDS_LENGTH*2, blank=False, null=False)
    ai_ships = models.CharField(max_length=FIELDS_LENGTH*2, blank=False, null=False)

    player = models.ForeignKey('auth.User')

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

    def update_player_board(self, x, y, state):
        self._update_board('player', x, y, state)

    def update_ai_board(self, x, y, state):
        self._update_board('ai', x, y, state)

    def hit_player_ship(self, x, y):
        return self._hit_ship('player', x, y)

    def hit_ai_ship(self, x, y):
        return self._hit_ship('ai', x, y)

    def game_over(self):
        filled = str(State.FILLED)

        if filled not in ''.join(json.loads(self.player_board)):
            return 'D'
        elif filled not in ''.join(json.loads(self.ai_board)):
            return 'V'

        return False

    def _update_board(self, owner, x, y, state):
        field_name = '{}_board'.format(owner)
        board = json.loads(getattr(self, field_name))
        row = list(board[x])

        row[y] = str(state)
        board[x] = ''.join(row)

        setattr(self, field_name, json.dumps(board))
        self.save()

    def _hit_ship(self, owner, x, y):
        ships_field_name = '{}_ships'.format(owner)
        board_field_name = '{}_board'.format(owner)
        ships = json.loads(getattr(self, ships_field_name))
        board = json.loads(getattr(self, board_field_name))
        point = [x, y]
        sunk = []
        state = State.HIT

        for ship in ships:
            if point in ship:
                if all(int(board[i][j]) == State.HIT for (i, j) in ship if [i, j] != point):
                    state = State.SUNK
                    sunk = ship

                    for x, y in ship:
                        if [x, y] != point:
                            self._update_board(owner, x, y, state)
                break

        setattr(self, ships_field_name, json.dumps(ships))
        self.save()
        self._update_board(owner, x, y, state)

        return state, sunk
