# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0005_auto_20151210_1048'),
    ]

    operations = [
        migrations.RenameModel('Proposal', 'TalkProposal'),
        migrations.AlterModelOptions(
            name='talkproposal',
            options={
                'verbose_name_plural': 'talk proposals',
                'verbose_name': 'talk proposal',
                'ordering': ['-created_at'],
            },
        ),
    ]
