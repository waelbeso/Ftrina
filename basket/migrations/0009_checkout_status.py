# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-19 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0008_auto_20180419_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]