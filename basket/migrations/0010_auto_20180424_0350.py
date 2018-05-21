# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-24 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0009_checkout_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='service_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='shipper_account',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
