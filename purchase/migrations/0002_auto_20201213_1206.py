# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-12-13 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasestatusmodel',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
