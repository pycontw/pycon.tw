from modeltranslation.translator import translator, TranslationOptions

from .models import Sponsor, OpenRole


class SponsorTranslationOptions(TranslationOptions):
    fields = ('intro',)


class OpenRoleTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(Sponsor, SponsorTranslationOptions)

translator.register(OpenRole, OpenRoleTranslationOptions)
