# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-27 04:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0034_auto_20180427_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 4, 27, 4, 43, 10, 117627, tzinfo=utc)),
        ),
    ]
