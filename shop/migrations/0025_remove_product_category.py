# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-03 01:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20180503_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]