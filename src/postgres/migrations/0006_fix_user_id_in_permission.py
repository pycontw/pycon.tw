from django.db import migrations


ALTER_PERMISSION_USER_ID = """
    ALTER TABLE "users_user_user_permissions" ALTER COLUMN "user_id"
        SET DATA TYPE bigint;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('postgres', '0005_fix_user_id_in_adminlog'),
    ]

    operations = [
        migrations.RunSQL(
            ALTER_PERMISSION_USER_ID,
            migrations.RunSQL.noop,
        )
    ]
