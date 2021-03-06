# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='cat_description',
            field=models.CharField(max_length=255, verbose_name='Category Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='cat_name',
            field=models.CharField(max_length=50, verbose_name='Category Name'),
        ),
    ]
