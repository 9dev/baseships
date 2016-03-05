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


class Game(models.Model):
    player_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
    ai_board = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
    player = models.ForeignKey('auth.User')

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})
