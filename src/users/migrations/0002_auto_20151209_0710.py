# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='', upload_to=users.models.photo_upload_to, verbose_name='photo', blank=True),
        ),
    ]
