from django.db import migrations, models

from core.models import BigForeignKey


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0036_add_proposal_update_timestamp'),
        ('reviews', '0015_review_appropriateness'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalkProposalSnapshot',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID',
                )),
                ('stage', models.IntegerField(
                    verbose_name='stage',
                )),
                ('dumped_json', models.TextField(
                    verbose_name='dumped JSON',
                )),
                ('dumped_at', models.DateTimeField(
                    auto_now=True,
                    verbose_name='dumped at',
                )),
                ('proposal', BigForeignKey(
                    on_delete=models.deletion.CASCADE,
                    to='proposals.TalkProposal',
                    verbose_name='proposal',
                )),
            ],
            options={
                'verbose_name': 'talk proposal snapshot',
                'verbose_name_plural': 'talk proposal snapshots',
            },
        ),
        migrations.AlterUniqueTogether(
            name='talkproposalsnapshot',
            unique_together={('proposal', 'stage')},
        ),
    ]
