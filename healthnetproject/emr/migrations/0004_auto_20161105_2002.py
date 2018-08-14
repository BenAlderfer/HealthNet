# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-05 20:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0003_auto_20161104_2244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='changeinstatus',
            options={'verbose_name': 'Status Change'},
        ),
        migrations.AlterModelOptions(
            name='prescription',
            options={'verbose_name': 'Prescription'},
        ),
        migrations.RemoveField(
            model_name='changeinstatus',
            name='reason',
        ),
        migrations.AddField(
            model_name='admission',
            name='reason',
            field=models.CharField(choices=[('SUR', 'Surgery'), ('EMER', 'Emergency'), ('OBS', 'Observation'), ('OTH', 'Other')], default='OTH', max_length=150, verbose_name='Reason'),
        ),
        migrations.AlterField(
            model_name='emritem',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='test',
            name='image',
            field=models.FileField(blank=True, max_length=200, upload_to='D:\\RIT projects\\SE 261\\Healthnet\\healthnetproject\\media/uploads/tests', verbose_name='Optional image'),
        ),
    ]