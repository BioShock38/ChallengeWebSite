# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('numero', models.IntegerField(unique=True)),
                ('truth', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='methods',
            field=models.CharField(default=b'Random', max_length=100),
        ),
        migrations.AddField(
            model_name='submission',
            name='simu',
            field=models.ForeignKey(default=1, to='challenge.Simulation'),
            preserve_default=False,
        ),
    ]
