# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-18 23:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0014_auto_20180418_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 4, 18, 23, 38, 26, 577932, tzinfo=utc)),
        ),
    ]