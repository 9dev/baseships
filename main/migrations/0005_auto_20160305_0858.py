# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160305_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='ai_board',
            field=models.CharField(max_length=320),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_board',
            field=models.CharField(max_length=320),
        ),
    ]
