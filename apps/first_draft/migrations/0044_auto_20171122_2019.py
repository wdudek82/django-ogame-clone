# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0043_auto_20171121_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='planet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='first_draft.Planet'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resource',
            name='location',
            field=models.IntegerField(choices=[(0, 'planetary surface'), (1, 'moon surface')], default=1),
        ),
    ]
