# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-29 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20190329_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price_new',
            new_name='new_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price_old',
            new_name='old_price',
        ),
    ]