from django.db import migrations


ALTER_GROUP_USER_ID = """
    ALTER TABLE "users_user_groups" alter COLUMN "user_id"
        SET DATA TYPE bigint;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
        ('postgres', '0007_fix_user_id_proposal_id_in_review'),
    ]

    operations = [
        migrations.RunSQL(
            ALTER_GROUP_USER_ID,
            migrations.RunSQL.noop,
        ),
    ]
