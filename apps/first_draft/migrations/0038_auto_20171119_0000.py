# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-18 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0037_auto_20171117_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='produced_per_hour',
        ),
        migrations.AddField(
            model_name='resource',
            name='capacity_exeeded',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]