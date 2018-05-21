# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-12 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0051_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.AddField(
            model_name='order',
            name='with_variant',
            field=models.BooleanField(default=False),
        ),
    ]
