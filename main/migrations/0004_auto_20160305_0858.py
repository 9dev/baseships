# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='owner',
        ),
        migrations.AlterField(
            model_name='game',
            name='ai_board',
            field=models.CharField(default='0', max_length=320),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_board',
            field=models.CharField(default='0', max_length=320),
        ),
        migrations.DeleteModel(
            name='Board',
        ),
    ]
