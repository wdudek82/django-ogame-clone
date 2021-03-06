# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0048_playerbuilding_new_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerbuilding',
            name='update_started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.IntegerField(choices=[(1, 'metal'), (2, 'crystal'), (3, 'deuterium')]),
        ),
    ]
