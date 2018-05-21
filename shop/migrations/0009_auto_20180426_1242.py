# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-26 12:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basket.Buyer'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Seller'),
        ),
    ]
