# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-04 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]