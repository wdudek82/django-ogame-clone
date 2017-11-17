# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0024_auto_20171116_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerresource',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='first_draft.PlayerPlanet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerresource',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
