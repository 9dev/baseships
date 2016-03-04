import json

from django.db import models


BOARD_SIZE = 2
FIELDS_LENGTH = len(json.dumps([[0] * BOARD_SIZE] * BOARD_SIZE))


class Board(models.Model):
    owner = models.ForeignKey('auth.User', null=True)
    fields = models.CharField(max_length=FIELDS_LENGTH, blank=False, null=False)
