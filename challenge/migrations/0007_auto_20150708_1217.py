# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0006_auto_20150708_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='methods',
            field=models.CharField(default=b'Random', max_length=200),
        ),
    ]
