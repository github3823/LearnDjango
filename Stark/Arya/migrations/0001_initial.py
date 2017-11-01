# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 03:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=128, unique=True)),
                ('key', models.TextField()),
                ('status', models.SmallIntegerField(choices=[(0, 'Waitting Approval'), (1, 'Accepted'), (2, 'Rejected')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('hosts', models.ManyToManyField(blank=True, to='Arya.Host')),
            ],
        ),
    ]
