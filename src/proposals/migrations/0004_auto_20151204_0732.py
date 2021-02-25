# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_auto_20151203_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='recording_policy',
            field=models.BooleanField(help_text='Whether you agree to give permission to PyCon Taiwan to record, edit, and release audio and video of your presentation.', default=True, choices=[(True, 'Yes'), (False, 'No')], verbose_name='recording policy'),
        ),
    ]
