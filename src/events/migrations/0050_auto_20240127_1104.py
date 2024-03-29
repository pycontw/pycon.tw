# Generated by Django 3.1.7 on 2024-01-27 03:04

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0049_rename_willing_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='joblistingsevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='keynoteevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='keynoteevent',
            name='speaker_photo',
            field=models.ImageField(default='', help_text="Raster format of the speaker's photo, e.g. PNG, JPEG.", storage=events.models.select_storage, upload_to=events.models.photo_upload_to, verbose_name='speaker photo'),
        ),
        migrations.AlterField(
            model_name='proposedtalkevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='proposedtutorialevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
        migrations.AlterField(
            model_name='sponsoredevent',
            name='conference',
            field=models.SlugField(choices=[('pycontw-2016', 'PyCon Taiwan 2016'), ('pycontw-2017', 'PyCon Taiwan 2017'), ('pycontw-2018', 'PyCon Taiwan 2018'), ('pycontw-2019', 'PyCon Taiwan 2019'), ('pycontw-2020', 'PyCon Taiwan 2020'), ('pycontw-2021', 'PyCon Taiwan 2021'), ('pycontw-2022', 'PyCon Taiwan 2022'), ('pycontw-2023', 'PyCon Taiwan 2023'), ('pycontw-2024', 'PyCon Taiwan 2024')], default='pycontw-2024', verbose_name='conference'),
        ),
    ]
