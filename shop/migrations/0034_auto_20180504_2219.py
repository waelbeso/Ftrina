# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-04 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_auto_20180504_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='currency',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='language',
            field=models.TextField(blank=True, choices=[('Arabic', 'Arabic'), ('English', 'English'), ('Chinese', 'Chinese'), ('French', 'French')], max_length=1, null=True),
        ),
    ]
