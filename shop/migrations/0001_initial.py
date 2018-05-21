# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-24 03:44
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

        ('basket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(default='+201005866658', max_length=128)),
                ('country', models.CharField(blank=True, max_length=13, null=True)),
                ('province', models.CharField(blank=True, max_length=55, null=True)),
                ('city', models.CharField(blank=True, max_length=55, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT(0.0 0.0)', null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('keywords', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.TextField(blank=True, choices=[('ar', 'Arabic'), ('en', 'English'), ('zh-hans', 'Chinese')], max_length=1, null=True)),
                ('classification', models.CharField(blank=True, default='product', max_length=55, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('code', models.CharField(blank=True, max_length=55, null=True)),
                ('user_limit', models.PositiveIntegerField(default=1)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('rate', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coverage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('country', models.CharField(blank=True, max_length=13, null=True)),
                ('province', models.CharField(blank=True, max_length=55, null=True)),
                ('city', models.CharField(blank=True, max_length=55, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('status', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('stage', models.CharField(blank=True, default='pending', max_length=55, null=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('o2o', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.Address')),
                ('basket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basket.Basket')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Coupon')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, max_length=64, null=True)),
                ('model_number', models.CharField(blank=True, max_length=55, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=55, null=True)),
                ('characteristics', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('description', models.TextField(null=True)),
                ('min_order', models.IntegerField(blank=True, null=True)),
                ('min_order_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('price_currency', models.CharField(blank=True, max_length=55, null=True)),
                ('supply_ability', models.IntegerField(blank=True, null=True)),
                ('supply_ability_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('supply_ability_time', models.CharField(blank=True, max_length=55, null=True)),
                ('lead_time', models.IntegerField(blank=True, null=True)),
                ('lead_time_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('payment_term', models.CharField(blank=True, max_length=55, null=True)),
                ('extras_term', models.CharField(blank=True, max_length=55, null=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('list_as', models.CharField(blank=True, max_length=55, null=True)),
                ('language', models.CharField(blank=True, max_length=55, null=True)),
                ('origin', models.CharField(blank=True, default='EG', max_length=55, null=True)),
                ('keywords', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('authority', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Servise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, max_length=64, null=True)),
                ('characteristics', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('description', models.TextField(null=True)),
                ('min_order', models.IntegerField(blank=True, null=True)),
                ('min_order_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=3, max_digits=19, null=True)),
                ('price_currency', models.CharField(blank=True, max_length=55, null=True)),
                ('supply_ability', models.IntegerField(blank=True, null=True)),
                ('supply_ability_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('supply_ability_time', models.CharField(blank=True, max_length=55, null=True)),
                ('lead_time', models.IntegerField(blank=True, null=True)),
                ('lead_time_unit', models.CharField(blank=True, max_length=55, null=True)),
                ('payment_term', models.CharField(blank=True, max_length=55, null=True)),
                ('extras_term', models.CharField(blank=True, max_length=55, null=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('coverage_term', models.CharField(blank=True, max_length=55, null=True)),
                ('list_as', models.CharField(blank=True, max_length=55, null=True)),
                ('language', models.CharField(blank=True, max_length=55, null=True)),
                ('keywords', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
                ('coverage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Coverage')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('specialty', models.CharField(blank=True, max_length=200, null=True)),
                ('keywords', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('language', models.TextField(blank=True, choices=[('ar', 'Arabic'), ('en', 'English'), ('zh-hans', 'Chinese'), ('fr', 'French')], max_length=1, null=True)),
                ('legalform', models.CharField(blank=True, max_length=100, null=True)),
                ('employees', models.CharField(blank=True, max_length=2, null=True)),
                ('activite', models.TextField(blank=True, choices=[('import', 'Import'), ('export', 'Export'), ('manufacturing', 'Manufacturing'), ('servisess', 'Servisess'), ('shipping', 'Shipping')], max_length=50, null=True)),
                ('areas', models.CharField(blank=True, max_length=200, null=True)),
                ('live', models.BooleanField(default=False)),
                ('country', models.CharField(blank=True, max_length=3, null=True)),
                ('province', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT(0.0 0.0)', null=True, srid=4326)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=55, null=True)),
                ('country', models.CharField(blank=True, max_length=13, null=True)),
                ('province', models.CharField(blank=True, max_length=55, null=True)),
                ('city', models.CharField(blank=True, max_length=55, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT(0.0 0.0)', null=True, srid=4326)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop')),
            ],
        ),
        migrations.AddField(
            model_name='servise',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='seller',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='servise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Servise'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='coverage',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='branch',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.CreateModel(
            name='ShopSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Shop Summary',
                'proxy': True,
                'verbose_name_plural': 'Shop Summary',
                'indexes': [],
            },
            bases=('shop.shop',),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set([('id', 'reference')]),
        ),
    ]
