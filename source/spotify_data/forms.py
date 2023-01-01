from django import forms
from spotify_data.models import SpotifyData

class DateRangeForm(forms.Form):
    FROM = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial="2019-01-01")
    TO = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial="2020-01-01")
    
class Artist1Form(forms.Form):
    ARTIST = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}), initial="Billie Eilish")

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
        self.fields['CHART'].choices = SpotifyData.objects.all().\
            only("chart").values_list("chart","chart").distinct().order_by("chart")

class RegionForm(forms.Form):
    REGION = forms.ChoiceField(required=True, choices=[], widget=forms.Select, initial="United States")

    def __init__(self, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        self.fields['REGION'].choices = SpotifyData.objects.all().\
            only("region").values_list("region","region").distinct().order_by("region")
