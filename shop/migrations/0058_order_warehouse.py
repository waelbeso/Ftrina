# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-14 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0057_order_max_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.WareHouse'),
        ),
    ]