# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0004_auto_20171115_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Universe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('speed', models.DecimalField(decimal_places=2, default=1, max_digits=4)),
            ],
        ),
        migrations.AddField(
            model_name='planet',
            name='max_temperature',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='planet',
            name='min_temperature',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='planet',
            name='name',
            field=models.CharField(default='a planet', max_length=30),
        ),
        migrations.AddField(
            model_name='planet',
            name='position',
            field=models.PositiveIntegerField(blank=True, choices=[(2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8)], null=True),
        ),
    ]
