# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0003_auto_20150702_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('desc', models.TextField()),
                ('rules', models.TextField()),
                ('evaluation', models.TextField()),
                ('lsimu', models.ManyToManyField(to='challenge.Simulation')),
            ],
        ),
    ]
