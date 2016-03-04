import json

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


class Board(models.Model):
    owner = models.ForeignKey('auth.User', null=True)
    fields = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
