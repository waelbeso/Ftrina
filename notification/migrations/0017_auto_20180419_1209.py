# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-19 12:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0016_auto_20180419_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 4, 19, 12, 9, 14, 122030, tzinfo=utc)),
        ),
    ]
