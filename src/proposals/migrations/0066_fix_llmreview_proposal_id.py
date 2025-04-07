from django.db import migrations
from django.db.models import deletion

from core.models import BigForeignKey


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0065_auto_20250327_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llmreview',
            name='proposal',
            field=BigForeignKey(
                on_delete=deletion.CASCADE,
                related_name='llm_review',
                to='proposals.talkproposal',
                verbose_name='proposal',
                unique=True,
            ),
        ),
    ]
