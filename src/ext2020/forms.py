from django import forms

from ext2020.models import Choice


class CommunityTrackForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"
