# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-05 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_auto_20180504_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='Status',
            field=models.TextField(choices=[('Active', 'Active'), ('Test', 'Test')], default='Test', max_length=1),
        ),
    ]
