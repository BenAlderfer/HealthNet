# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-05 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0005_auto_20161107_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='reason',
            field=models.CharField(choices=[('SUR', 'Surgery'), ('EMER', 'Emergency'), ('OBS', 'Observation'), ('OTH', 'Other')], default='OTH', max_length=150, verbose_name='Reason'),
        ),
    ]
