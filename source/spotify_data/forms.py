from django import forms

class DateForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

class CharFieldForm(forms.Form):
    artist = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'type':'charfield'}))