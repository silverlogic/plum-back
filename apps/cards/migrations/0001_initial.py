# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-16 18:45
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.PositiveIntegerField()),
                ('name_on_card', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=20)),
                ('expiration_date', models.DateField(help_text='Day is ignored.')),
                ('type', models.CharField(choices=[('C', 'Credit'), ('P', 'Prepaid'), ('D', 'Prepaid'), ('R', 'Deferred Debt'), ('H', 'Charge Card')], max_length=100)),
                ('sub_type', models.CharField(choices=[('N', 'Non-Reloadable'), ('R', 'Reloadable')], max_length=100)),
                ('owner_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
