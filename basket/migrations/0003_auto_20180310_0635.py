# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-10 06:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0002_auto_20180310_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]