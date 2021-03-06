# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('first_draft', '0017_auto_20171116_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='playerplanet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerplanet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='playerplanet',
            name='moon',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='first_draft.Moon', null=True, blank=True),
            preserve_default=False,
        ),
    ]
