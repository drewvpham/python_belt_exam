# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-31 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam', '0002_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(),
        ),
    ]