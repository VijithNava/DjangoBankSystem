# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 02:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20160314_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]