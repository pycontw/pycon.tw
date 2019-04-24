from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import override
from django.utils.text import slugify
from ordered_model.models import OrderedModel

from core.models import ConferenceRelated


def logo_upload_to(instance, filename):
    return 'sponsors/{name}/{filename}'.format(
        name=slugify(instance.name, allow_unicode=True),
        filename=filename,
    )


class Sponsor(ConferenceRelated, OrderedModel):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
    )
    website_url = models.URLField(
        verbose_name=_('website URL'),
        max_length=255, blank=True,
    )
    intro = models.TextField(
        verbose_name=_('introduction'),
    )
    logo_svg = models.FileField(
        verbose_name=_('logo (SVG)'),
        blank=True, upload_to=logo_upload_to,
        help_text=_(
            "Vector format of the logo, in SVG. This takes precedence to the "
            "raster format, if available."
        ),
    )
    logo_image = models.ImageField(
        verbose_name=_('logo (image)'),
        db_column='logo',  # Backward compatibility.
        blank=True, upload_to=logo_upload_to,
        help_text=_(
            "Raster format of the logo, e.g. PNG, JPEG. This is used as "
            "fallback when the SVG file is not available."
        ),
    )

    class Level:
        PLATINUM = 1
        GOLD = 2
        SILVER = 3
        BRONZE = 4
        SPECIAL = 5
        ORGANIZER = 6
        COORGANIZER = 7

        # Backward compatibility.
        PARTNER = COORGANIZER

    LEVEL_CHOICES = (
        (Level.PLATINUM, _('platinum')),
        (Level.GOLD, _('gold')),
        (Level.SILVER, _('silver')),
        (Level.BRONZE, _('bronze')),
        (Level.SPECIAL, _('special')),
        (Level.ORGANIZER, _('organizer')),
        (Level.COORGANIZER, _('co-organizer')),
    )

    @property
    def level_en_name(self):
        with override('en-us'):
            return self.get_level_display()

    level = models.SmallIntegerField(
        verbose_name=_('level'),
        choices=LEVEL_CHOICES,
    )

    class Meta(OrderedModel.Meta):
        verbose_name = _('sponsor')
        verbose_name_plural = _('sponsors')
        ordering = ('order',)

    def __str__(self):
        return self.name

    @property
    def logo(self):
        return self.logo_svg or self.logo_image or None
