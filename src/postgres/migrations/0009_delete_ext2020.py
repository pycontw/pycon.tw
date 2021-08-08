from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
        ('postgres', '0008_fix_user_id_group'),
    ]

    operations = [
        migrations.RunSQL('''
        drop table if exists ext2020;
        delete from auth_permission where content_type_id in (select id from django_content_type where app_label = '{app_label}');
        delete from django_admin_log where content_type_id in (select id from django_content_type where app_label = '{app_label}');
        delete from django_content_type where app_label = '{app_label}';
        delete from django_migrations where app='{app_label}';
        '''.format(app_label='ext2020'))
    ]
