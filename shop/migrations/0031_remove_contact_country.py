# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-04 18:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_contact_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='country',
        ),
    ]
