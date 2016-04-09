from modeltranslation.translator import translator, TranslationOptions

from .models import Sponsor


class SponsorTranslationOptions(TranslationOptions):
    fields = ('intro',)

translator.register( Sponsor, SponsorTranslationOptions )
