# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 12:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0052_remove_planet_free_sufrace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moon',
            name='planet',
        ),
        migrations.RemoveField(
            model_name='planet',
            name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='playerbuilding',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='playerbuilding',
            name='building',
        ),
        migrations.RemoveField(
            model_name='playerbuilding',
            name='planet',
        ),
        migrations.RemoveField(
            model_name='playerprofile',
            name='universe',
        ),
        migrations.RemoveField(
            model_name='playerprofile',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='resource',
            name='planet',
        ),
        migrations.DeleteModel(
            name='Moon',
        ),
        migrations.DeleteModel(
            name='Planet',
        ),
        migrations.DeleteModel(
            name='PlayerBuilding',
        ),
        migrations.DeleteModel(
            name='PlayerProfile',
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]
