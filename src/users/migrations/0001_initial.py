# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, db_index=True, unique=True, verbose_name='email address')),
                ('speaker_name', models.CharField(max_length=100, verbose_name='speaker name')),
                ('bio', models.TextField(max_length=140, help_text='About you. There will be no formatting.', verbose_name='biography')),
                ('photo', models.FileField(upload_to='documents/%Y/%m/%d', default='', blank=True, verbose_name='photo')),
                ('twitter_id', models.CharField(max_length=100, blank=True, verbose_name='twitter')),
                ('github_id', models.CharField(max_length=100, blank=True, verbose_name='github')),
                ('facebook_id', models.CharField(max_length=100, blank=True, verbose_name='facebook')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', blank=True, related_name='user_set', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', blank=True, related_name='user_set', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
        ),
    ]
