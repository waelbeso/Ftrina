# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-29 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_product_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='value',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]