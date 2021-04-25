from modeltranslation.translator import translator, TranslationOptions

from .models import Sponsor, OpenRole


class SponsorTranslationOptions(TranslationOptions):
    fields = ('intro', 'subtitle',)


class OpenRoleTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'requirements',)


translator.register(Sponsor, SponsorTranslationOptions)

translator.register(OpenRole, OpenRoleTranslationOptions)
