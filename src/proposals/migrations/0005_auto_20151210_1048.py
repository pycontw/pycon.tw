# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20151204_0732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='objectives',
        ),
        migrations.AlterField(
            model_name='proposal',
            name='abstract',
            field=models.TextField(help_text='The overview of what the talk is about. If the talk assume some domain knowledge please state it here. If yout talk is accepted, this will be displayed on both the website and the handbook. Should be one paragraph.', verbose_name='abstract', max_length=400),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='detailed_description',
            field=models.TextField(help_text="Description of your talk. Will be made public if your proposal is accepted. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.", verbose_name='detailed description'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='outline',
            field=models.TextField(help_text="Tell the reviewers about your talk. Try not be too lengthy, or you could scare away many reviewers. A comfortable length is less than 1000 characters (or about 650 Chinese characters). Including related links will help reviewers understand and more likely accept the proposal. Note that most reviewers may not understand the topic as deeply as you do. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.", verbose_name='outline'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='supplementary',
            field=models.TextField(default='', help_text="Anything else you'd like the program committee to know when making their selection: your past speaking experience, community experience, etc. This is not made public. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.", verbose_name='supplementary', blank=True),
        ),
    ]
