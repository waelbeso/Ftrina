# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-27 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0067_invoice_commercial_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='commercial_invoice',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
