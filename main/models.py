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

    def _update_board(self, owner, x, y, state):
        field_name = '{}_board'.format(owner)
        board = json.loads(getattr(self, field_name))
        row = list(board[x])

        row[y] = str(state)
        board[x] = ''.join(row)

        setattr(self, field_name, json.dumps(board))
        self.save()
