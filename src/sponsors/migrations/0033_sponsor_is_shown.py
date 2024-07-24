# Generated by Django 3.2.25 on 2024-06-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0032_fix_verbose_typo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='is_shown',
            field=models.BooleanField(default=False, verbose_name='is shown'),
        ),
    ]