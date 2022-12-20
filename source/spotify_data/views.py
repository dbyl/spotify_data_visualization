import plotly.express as px
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData

def home(request):
    return render(request, 'base.html')