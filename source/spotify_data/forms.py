from django import forms
from .models import *

from spotify_data.models import (Region,
                                 Rank,
                                 Chart,
                                 Artist,
                                 Title,
                                 SpotifyData)

    
class RankChartForm(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2018-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    region = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Drake")
    title = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="God's Plan")

    def __init__(self, *args, **kwargs):
        super(RankChartForm, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")
        self.fields['region'].choices = Region.objects.values("id").\
            values_list("id","name")
        self.fields['region'].initial = 68


class RankChart2Form(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2020-01-01")
    region = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Drake")
    title = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="God's Plan")
    artist_2 = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Billie Eilish")
    title_2 = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="bad guy")

    def __init__(self, *args, **kwargs):
        super(RankChart2Form, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")
        self.fields['region'].choices = Region.objects.values("id").\
            values_list("id","name")
        self.fields['region'].initial = 68


class PopularityChartForm(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2018-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    region = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Drake")
    top_rank = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))

    def __init__(self, *args, **kwargs):
        super(PopularityChartForm, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")
        self.fields['region'].choices = Region.objects.values("id").\
            values_list("id","name")
        self.fields['top_rank'].choices = Rank.objects.values("id").\
            values_list("id","name")
        self.fields['region'].initial = 68

class PopularityChartForm2(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2018-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    region = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Drake")
    artist_2 = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Kanye West")
    top_rank = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))

    def __init__(self, *args, **kwargs):
        super(PopularityChartForm2, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")
        self.fields['region'].choices = Region.objects.values("id").\
            values_list("id","name")
        self.fields['top_rank'].choices = Rank.objects.values("id").\
            values_list("id","name")
        self.fields['region'].initial = 68
        self.fields['top_rank'].initial = 20

class ArtistMapPopularityForm(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2018-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Drake")

    def __init__(self, *args, **kwargs):
        super(ArtistMapPopularityForm, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")

class SongMapPopularityForm(forms.Form):

    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2018-01-01")
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'form_widgets'}), initial="2019-01-01")
    chart = forms.ChoiceField(required=True, choices=[], widget=forms.Select(attrs={'class':'form_widgets'}))
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="Dua Lipa")
    title = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield', 'class':'form_widgets'}), initial="New Rules")

    def __init__(self, *args, **kwargs):
        super(SongMapPopularityForm, self).__init__(*args, **kwargs)
        self.fields['chart'].choices = Chart.objects.values("id").\
            values_list("id","name")
