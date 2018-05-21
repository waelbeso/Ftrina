# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-06 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_auto_20180506_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cart_description',
            field=models.CharField(blank=True, default='Product', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='new', null=True),
        ),
    ]
