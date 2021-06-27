from modeltranslation.translator import translator, TranslationOptions

from .models import KeynoteEvent


class KeynoteEventTranslationOptions(TranslationOptions):
    fields = ('speaker_name', 'speaker_bio', 'session_title', 'session_description')


translator.register(KeynoteEvent, KeynoteEventTranslationOptions)
