# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-29 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20180428_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
