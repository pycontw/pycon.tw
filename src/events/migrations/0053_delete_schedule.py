# Generated by Django 3.2.25 on 2024-04-15 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0052_remove_sponsoredevent_prefer_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]