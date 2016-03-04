# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20160304_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ai_board', models.ForeignKey(to='main.Board', related_name='ai_board')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('player_board', models.ForeignKey(to='main.Board', related_name='user_board')),
            ],
        ),
    ]
