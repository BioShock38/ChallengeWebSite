# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0004_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='isover',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='simulation',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='challenge',
            field=models.ForeignKey(default=1, to='challenge.Challenge'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 8, 8, 42, 16, 39922, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
