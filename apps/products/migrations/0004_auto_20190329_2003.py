# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-29 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190329_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='more',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='content',
            field=models.TextField(max_length=1000),
        ),
    ]
