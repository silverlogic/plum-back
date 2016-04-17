# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_auto_20160417_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('merchant_name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('declined', 'Declined')], max_length=50)),
                ('when', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='amount_on_card',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='card',
            name='amount_spent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Card'),
        ),
    ]