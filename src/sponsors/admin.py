from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from modeltranslation.admin import TranslationAdmin

from .models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(TranslationAdmin, OrderedModelAdmin):
    fields = [
        'name', 'level', 'website_url', 'intro',
        'logo_svg', 'logo_image',
    ]
    list_display = ['order', 'name', 'level', 'move_up_down_links']
    list_filter = ['level']
