from django.apps import AppConfig as BaseAppConfig
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    """Default config for the remotedb app.
    """
    name = 'remotedb'
    verbose_name = _('Remote DB')

    def ready(self):
        from . import triggers

        def sync_sponsored_talk_detail(sender, instance, *args, **kwargs):
            triggers.sync_sponsored_talk_detail(instance)

        def sync_proposal_detail(sender, instance, *args, **kwargs):
            triggers.sync_proposal_detail(instance)

        def sync_schedule(*args, **kwargs):
            triggers.sync_schedule()

        def sync_user_events(sender, instance, *args, **kwargs):
            triggers.sync_user_events(instance)

        post_save.connect(
            sync_proposal_detail,
            sender='events.Schedule',
            weak=False,
        )
        post_save.connect(
            sync_sponsored_talk_detail,
            sender='events.SponsoredEvent',
            weak=False,
        )
        post_save.connect(
            sync_proposal_detail,
            sender='proposals.TalkProposal',
            weak=False,
        )
        post_save.connect(
            sync_user_events,
            sender=settings.AUTH_USER_MODEL,
            weak=False,
        )
