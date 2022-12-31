from django import forms

CHART_CHOICES = (("top200","top200"), ("viral50", "viral50"))

class DateForm(forms.Form):
    FROM = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    TO = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    
class ArtistTitle(forms.Form):
    ARTIST = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))
    TITLE = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))

class ChartRegion(forms.Form):
    CHART = forms.ChoiceField(choices=CHART_CHOICES)