# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0002_auto_20151202_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposal',
            options={'verbose_name': 'proposal', 'ordering': ['-created_at'], 'verbose_name_plural': 'proposals'},
        ),
        migrations.AddField(
            model_name='proposal',
            name='created_at',
            field=models.DateTimeField(verbose_name='created at', auto_now_add=True, db_index=True, default=datetime.datetime(2015, 12, 3, 3, 26, 48, 592213, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
