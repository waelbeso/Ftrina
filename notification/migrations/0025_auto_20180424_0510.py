# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-24 05:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0024_auto_20180424_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 4, 24, 5, 10, 18, 308102, tzinfo=utc)),
        ),
    ]
