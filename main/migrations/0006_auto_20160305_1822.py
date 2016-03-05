# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160305_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ai_ships',
            field=models.CharField(max_length=640, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='player_ships',
            field=models.CharField(max_length=640, default=''),
            preserve_default=False,
        ),
    ]
