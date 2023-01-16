from django import forms
from .models import *
from spotify_data.models import (Region,
                                 Rank,
                                 Chart,
                                 Artist,
                                 Title,
                                 SpotifyData)

class DateRangeForm(forms.Form):
    FROM = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial="2019-01-01")
    TO = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial="2020-01-01")
    
class Artist1Form(forms.Form):

    ARTIST = forms.ChoiceField(required=True, choices=[], widget=forms.Select,)

    def __init__(self, *args, **kwargs):
        super(Artist1Form, self).__init__(*args, **kwargs)
        self.fields['ARTIST'].choices = Artist.objects.values("name").\
            values_list("name","name")

class Title1Form(forms.Form):
    TITLE = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}), initial="bad guy")

class Artist2Form(forms.Form):
    ARTIST_2 = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))

class Title2Form(forms.Form):
    TITLE_2 = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))

class ChartForm(forms.Form):
    CHART = forms.ChoiceField(required=True, choices=[], widget=forms.Select,)

    def __init__(self, *args, **kwargs):
        super(ChartForm, self).__init__(*args, **kwargs)
        self.fields['CHART'].choices = Chart.objects.values("name").\
            values_list("name","name")

class RegionForm(forms.Form):
    REGION = forms.ChoiceField(required=True, choices=[], widget=forms.Select,)

    def __init__(self, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        self.fields['REGION'].choices = Region.objects.values("name").\
            values_list("name","name")

class ArtistTitleForm(forms.ModelForm):
    class Meta:
        model = SpotifyData
        fields = ['artist','title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].queryset = Title.objects.none()

        if 'artist' in self.data:
            try:
                artist_id = int(self.data.get('artist'))
                self.fields['title'].queryset = Title.objects.filter(artist_id=artist_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['title'].queryset = self.instance.artist.title_set.order_by('title')


