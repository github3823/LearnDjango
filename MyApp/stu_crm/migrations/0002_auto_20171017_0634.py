# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='ptone',
        ),
        migrations.AddField(
            model_name='customer',
            name='pone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
