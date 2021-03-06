# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0021_playerbuilding_building_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerbuilding',
            old_name='upgrade_end',
            new_name='upgrade_ends',
        ),
        migrations.AlterUniqueTogether(
            name='playerbuilding',
            unique_together=set([('player', 'players_planet', 'building_location', 'building')]),
        ),
    ]
