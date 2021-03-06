# Generated by Django 3.1.7 on 2021-07-18 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0036_alter_keynoteevent_'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='joblistingsevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='keynoteevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='proposedtalkevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='proposedtutorialevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='sponsoredevent',
            name='location',
            field=models.CharField(blank=True, choices=[('2-all', 'All rooms'), ('3-r012', 'R0, R1, R2'), ('4-r0', 'R0'), ('5-r1', 'R1'), ('6-r2', 'R2'), ('1-r3', 'R3'), ('7-r4', 'Open Space'), ('8-oth', 'Other')], db_index=True, max_length=6, null=True, verbose_name='location'),
        ),
    ]
