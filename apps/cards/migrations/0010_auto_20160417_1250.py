# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_auto_20160417_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='cards.Card'),
        ),
    ]
