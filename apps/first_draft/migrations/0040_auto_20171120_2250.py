# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0039_remove_resource_capacity_exeeded'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='new_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='amount',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
