# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-13 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0056_auto_20180513_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='max_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]