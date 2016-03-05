import json

from django.core.urlresolvers import reverse
from django.db import models


BOARD_SIZE = 10
FIELDS_LENGTH = len(json.dumps([[0] * BOARD_SIZE] * BOARD_SIZE))

SHIPS = {
    5: 1,
    4: 1,
    3: 1,
    2: 2,
    1: 2,
}


class State(object):
    EMPTY = 0
    FILLED = 1
    MISSED = 2
    HIT = 3


class Game(models.Model):
    player_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
    ai_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
    player = models.ForeignKey('auth.User')

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

    def update_player_board(self, x, y, state):
        player_board = json.loads(self.player_board)
        row = list(player_board[x])

        row[y] = str(state)
        player_board[x] = ''.join(row)

        self.player_board = json.dumps(player_board)
        self.save()
