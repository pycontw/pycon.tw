# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def check_user_1(apps, schema_editor):
    Proposal = apps.get_model('proposals', 'Proposal')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    if Proposal.objects.exists() and not User.objects.filter(pk=1).exists():
        raise ImproperlyConfigured(
            'Default user with pk=1 is needed for this migration.'
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(verbose_name=b'title', max_length=140)),
                ('category', models.CharField(choices=[(b'PRAC', b'Best Practices & Patterns'), (b'COM', b'Community'), (b'DB', b'Databases'), (b'DATA', b'Data Analysis'), (b'EDU', b'Education'), (b'EMBED', b'Embedd Systems'), (b'GAME', b'Gaming'), (b'OTHER', b'Other'), (b'CORE', b'Python Core & Internals (language, stdlib, etc.)'), (b'LIBS', b'Python Libraries'), (b'SCI', b'Science'), (b'SEC', b'Security'), (b'ADMIN', b'Systems Administration'), (b'TEST', b'Testing'), (b'WEB', b'Web Frameworks')], verbose_name=b'category', max_length=5)),
                ('duration', models.CharField(choices=[(b'NOPREF', b'No preference'), (b'PREF25', b'Prefer 25min'), (b'PREF45', b'Prefer 45min')], verbose_name=b'duration', max_length=6)),
                ('language', models.CharField(choices=[(b'ENG', b'English'), (b'CHI', b'Chinese')], verbose_name=b'language', max_length=3)),
                ('target_audience', models.CharField(verbose_name=b'target audience', max_length=140, help_text=b'Who is the intended audience for your talk? (Be specific, "Python users" is not a good answer)')),
                ('abstract', models.TextField(verbose_name=b'abstract', max_length=400, help_text=b'The overview of what the talk is about. If the talk assume some domain knowledge please state it here.')),
                ('python_level', models.CharField(choices=[(b'NOVICE', b'Novice'), (b'INTERMEDIATE', b'Intermediate'), (b'EXPERIENCED', b'Experienced')], verbose_name=b'python level', max_length=12, help_text=b'The choice of talk level matters during the review process. More definition of talk level can be found at the Talk Level Definition in [How to Propose a talk] page. Note that a proposal who\'t be more likely to accepted because of being "Novice" level. We may contact you to change the talk level when we find the contend is too-hard or too-easy for the target audience.')),
                ('objectives', models.TextField(verbose_name=b'objectives', help_text=b"What will attendees get out of your talk? When they leave the room, what will they know that they didn't know before?")),
                ('detailed_description', models.TextField(verbose_name=b'detailed description', help_text=b'Try not be too lengthy which will scare away many reviewers. A comfortable length is less than 1000 chars (about 650 Chinese chars). Including related links to the talk topic will help reviewers understand and more likely accept the proposal. Note that most reviewers may not understand the topic as deep as you do.')),
                ('outline', models.TextField(verbose_name=b'outline', default=b'', help_text=b'How the talk will be arranged. It is highly recommended to attach the estimated time length for each sections in the talk. Talks in favor of 45min should have a fallback plan about how to shrink the content into a 25min one.', blank=True)),
                ('supplementary', models.TextField(verbose_name=b'supplementary', default=b'', help_text=b"Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc.", blank=True)),
                ('recording_policy', models.BooleanField(choices=[(True, b'Yes'), (False, b'No')], verbose_name=b'recording policy', max_length=1, help_text=b'Description: If you agree to give permission to PyCon Taiwan to record, edit, and release audio and video of your presentation, please check this box. See [Recoding Release] for details.')),
                ('slide_link', models.URLField(blank=True, verbose_name=b'slide link', default=b'', help_text=b'You can add your slide link near or after the conference day. Not required for review.')),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
            },
        ),
        migrations.AlterModelOptions(
            name='proposal',
            options={'verbose_name': 'proposal', 'verbose_name_plural': 'proposals'},
        ),
        migrations.AlterField(
            model_name='proposal',
            name='abstract',
            field=models.TextField(verbose_name='abstract', max_length=400, help_text='The overview of what the talk is about. If the talk assume some domain knowledge please state it here.'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='category',
            field=models.CharField(choices=[('PRAC', 'Best Practices & Patterns'), ('COM', 'Community'), ('DB', 'Databases'), ('DATA', 'Data Analysis'), ('EDU', 'Education'), ('EMBED', 'Embedd Systems'), ('GAME', 'Gaming'), ('OTHER', 'Other'), ('CORE', 'Python Core & Internals (language, stdlib, etc.)'), ('LIBS', 'Python Libraries'), ('SCI', 'Science'), ('SEC', 'Security'), ('ADMIN', 'Systems Administration'), ('TEST', 'Testing'), ('WEB', 'Web Frameworks')], verbose_name='category', max_length=5),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='detailed_description',
            field=models.TextField(verbose_name='detailed description', help_text='Try not be too lengthy which will scare away many reviewers. A comfortable length is less than 1000 chars (about 650 Chinese chars). Including related links to the talk topic will help reviewers understand and more likely accept the proposal. Note that most reviewers may not understand the topic as deep as you do.'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='duration',
            field=models.CharField(choices=[('NOPREF', 'No preference'), ('PREF25', 'Prefer 25min'), ('PREF45', 'Prefer 45min')], verbose_name='duration', max_length=6),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='language',
            field=models.CharField(choices=[('ENG', 'English'), ('CHI', 'Chinese')], verbose_name='language', max_length=3),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='objectives',
            field=models.TextField(verbose_name='objectives', help_text="What will attendees get out of your talk? When they leave the room, what will they know that they didn't know before?"),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='outline',
            field=models.TextField(verbose_name='outline', default='', help_text='How the talk will be arranged. It is highly recommended to attach the estimated time length for each sections in the talk. Talks in favor of 45min should have a fallback plan about how to shrink the content into a 25min one.', blank=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='python_level',
            field=models.CharField(choices=[('NOVICE', 'Novice'), ('INTERMEDIATE', 'Intermediate'), ('EXPERIENCED', 'Experienced')], verbose_name='python level', max_length=12, help_text='The choice of talk level matters during the review process. More definition of talk level can be found at the Talk Level Definition in [How to Propose a talk] page. Note that a proposal who\'t be more likely to accepted because of being "Novice" level. We may contact you to change the talk level when we find the contend is too-hard or too-easy for the target audience.'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='recording_policy',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='recording policy', max_length=1, help_text='Description: If you agree to give permission to PyCon Taiwan to record, edit, and release audio and video of your presentation, please check this box. See [Recoding Release] for details.'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='slide_link',
            field=models.URLField(blank=True, verbose_name='slide link', default='', help_text='You can add your slide link near or after the conference day. Not required for review.'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='supplementary',
            field=models.TextField(verbose_name='supplementary', default='', help_text="Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc.", blank=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='target_audience',
            field=models.CharField(verbose_name='target audience', max_length=140, help_text='Who is the intended audience for your talk? (Be specific, "Python users" is not a good answer)'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(verbose_name='title', max_length=140),
        ),
        migrations.RunPython(
            code=check_user_1,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddField(
            model_name='proposal',
            name='submitter',
            field=models.ForeignKey(verbose_name='submitter', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
