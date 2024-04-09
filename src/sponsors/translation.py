from modeltranslation.translator import TranslationOptions, translator

from .models import OpenRole, Sponsor


class SponsorTranslationOptions(TranslationOptions):
    fields = ('name', 'intro', 'subtitle',)
    required_languages = {'default': ('name',)}


class OpenRoleTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'requirements',)


translator.register(Sponsor, SponsorTranslationOptions)

translator.register(OpenRole, OpenRoleTranslationOptions)
