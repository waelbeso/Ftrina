# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-05 20:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_shop_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='Status',
            new_name='status',
        ),
    ]
