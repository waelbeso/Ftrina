# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-12 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0053_option'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='with_variant',
            new_name='with_option',
        ),
    ]
