# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 20:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0015_auto_20171116_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerplanet',
            old_name='name',
            new_name='planet_name',
        ),
    ]
