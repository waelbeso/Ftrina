# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-23 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0062_variant_usd_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='usd_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
