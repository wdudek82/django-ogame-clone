# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 20:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0033_auto_20171117_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='produced_per_hour',
        ),
    ]