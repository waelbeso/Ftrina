# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-24 02:50
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Future_Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='Name', max_length=55, null=True)),
                ('email', models.EmailField(blank=True, default='email', max_length=55, null=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, default='+201005866658', max_length=128, null=True)),
            ],
        ),
    ]
