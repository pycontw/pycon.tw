#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations


def update_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    site = Site.objects.using(db_alias).order_by('pk').first()
    site.domain = site.name = 'tw.pycon.org'
    site.save()


def revert_default_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    site = Site.objects.using(db_alias).order_by('pk').first()
    site.domain = site.name = 'examples.com'
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(
            code=update_default_site,
            reverse_code=revert_default_site,
        )
    ]
