# Generated by Django 3.2.25 on 2024-07-30 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0033_sponsor_is_shown'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='level',
            field=models.SmallIntegerField(choices=[(0, 'diamond'), (1, 'platinum'), (2, 'gold'), (3, 'silver'), (4, 'bronze'), (5, 'special'), (6, 'special-thanks'), (7, 'organizer'), (8, 'co-organizer'), (9, 'sprint-co-organizer')], verbose_name='level'),
        ),
    ]
