from django import forms


from ext2020.models import Venue



class CommunityTrackForm(forms.Form):
    venue = forms.ModelChoiceField(queryset=Venue.objects.all())
    attendee_token = forms.CharField()
    selected_time = forms.DateTimeField()
