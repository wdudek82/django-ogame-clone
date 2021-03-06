# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.PositiveIntegerField()),
                ('free_sufrace', models.PositiveIntegerField()),
                ('base_production', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlanetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='Resources',
            new_name='Resource',
        ),
        migrations.AddField(
            model_name='planettype',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_draft.Resource'),
        ),
        migrations.AddField(
            model_name='planet',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_draft.PlanetType'),
        ),
    ]
