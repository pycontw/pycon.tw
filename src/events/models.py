from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BigForeignKey, EventInfo


class SponsoredEvent(EventInfo):

    host = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('host'),
    )
    slug = models.SlugField(
        allow_unicode=True,
        verbose_name=_('slug'),
    )

    class Meta:
        verbose_name = _('sponsored event')
        verbose_name_plural = _('sponsored events')

    def get_absolute_url(self):
        return reverse('events_sponsored_event_detail', kwargs={
            'slug': self.slug,
        })
