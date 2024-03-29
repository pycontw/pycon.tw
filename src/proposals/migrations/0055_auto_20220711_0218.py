# Generated by Django 3.1.7 on 2022-07-10 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0054_auto_20220227_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkproposal',
            name='language',
            field=models.CharField(choices=[('ENEN', 'English talk'), ('ZHEN', 'Chinese talk w. English slides'), ('JPEN', 'Japanese talk w. English slides'), ('NONEN', 'non-English talk w. English slides')], max_length=5, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='tutorialproposal',
            name='language',
            field=models.CharField(choices=[('ENEN', 'English talk'), ('ZHEN', 'Chinese talk w. English slides'), ('JPEN', 'Japanese talk w. English slides'), ('NONEN', 'non-English talk w. English slides')], max_length=5, verbose_name='language'),
        ),
    ]
