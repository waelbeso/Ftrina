# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-04 20:06
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_contact_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+201005866658', max_length=128),
        ),
    ]