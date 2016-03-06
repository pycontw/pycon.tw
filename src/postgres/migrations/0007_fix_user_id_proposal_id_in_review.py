from django.db import migrations


ALTER_REVIEW_PROPOSAL_ID = """
    ALTER TABLE "reviews_review" alter COLUMN "proposal_id"
        SET DATA TYPE bigint;
"""

ALTER_REVIEW_REVIEWER_ID = """
    ALTER TABLE "reviews_review" alter COLUMN "reviewer_id"
        SET DATA TYPE bigint;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
        ('postgres', '0006_fix_user_id_in_permission'),
    ]

    operations = [
        migrations.RunSQL(
            ALTER_REVIEW_PROPOSAL_ID,
            migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            ALTER_REVIEW_REVIEWER_ID,
            migrations.RunSQL.noop,
        ),
    ]
