# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-09 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_auto_20180509_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
