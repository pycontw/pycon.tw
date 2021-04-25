# Generated by Django 3.1.7 on 2021-04-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0024_auto_20210406_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='openrole',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021')], default='pycontw-2021', verbose_name='conference'),
        ),
        migrations.AddField(
            model_name='openrole',
            name='name_en_us',
            field=models.CharField(max_length=100, null=True, verbose_name='open role name'),
        ),
        migrations.AddField(
            model_name='openrole',
            name='name_zh_hant',
            field=models.CharField(max_length=100, null=True, verbose_name='open role name'),
        ),
        migrations.AddField(
            model_name='openrole',
            name='requirements',
            field=models.TextField(null=True, verbose_name='open role requirements'),
        ),
        migrations.AddField(
            model_name='openrole',
            name='requirements_en_us',
            field=models.TextField(null=True, verbose_name='open role requirements'),
        ),
        migrations.AddField(
            model_name='openrole',
            name='requirements_zh_hant',
            field=models.TextField(null=True, verbose_name='open role requirements'),
        ),
    ]