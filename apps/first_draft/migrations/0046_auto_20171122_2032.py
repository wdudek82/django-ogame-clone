# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 19:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0045_auto_20171122_2030'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('resource_type', 'planet', 'location')]),
        ),
    ]