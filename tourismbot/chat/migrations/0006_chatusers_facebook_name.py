# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-10 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20170310_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatusers',
            name='facebook_name',
            field=models.CharField(default='name', max_length=100),
        ),
    ]