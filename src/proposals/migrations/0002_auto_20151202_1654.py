# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='recording_policy',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='recording policy', help_text='Description: If you agree to give permission to PyCon Taiwan to record, edit, and release audio and video of your presentation, please check this box. See [Recoding Release] for details.', default=True),
        ),
    ]
