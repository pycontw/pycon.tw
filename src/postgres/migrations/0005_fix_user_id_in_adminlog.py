from django.db import migrations


ALTER_LOGENTRY_USER_ID = """
    ALTER TABLE "django_admin_log" ALTER COLUMN "user_id"
        SET DATA TYPE bigint;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        ('postgres', '0004_user_generated_id'),
    ]

    operations = [
        migrations.RunSQL(
            ALTER_LOGENTRY_USER_ID,
            migrations.RunSQL.noop,
        )
    ]
