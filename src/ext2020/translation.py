from modeltranslation.translator import translator, TranslationOptions

from .models import Venue


class VenueTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'community', )


translator.register(Venue, VenueTranslationOptions)
