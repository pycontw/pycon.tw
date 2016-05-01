from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from core.models import BigForeignKey, EventInfo


class SponsoredEvent(EventInfo):

    host = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('host'),
    )

    class Meta:
        verbose_name = _('sponsored event')
        verbose_name_plural = _('sponsored events')
