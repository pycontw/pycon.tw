from modeltranslation.translator import translator, TranslationOptions

from .models import Venue, CommunityTrackEvent


class VenueTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'community', )


class CommunityTrackEventTranslationOptions(TranslationOptions):
    fields = ('custom_event', )


translator.register(Venue, VenueTranslationOptions)
translator.register(CommunityTrackEvent, CommunityTrackEventTranslationOptions)
