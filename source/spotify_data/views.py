import plotly.express as px
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData


def index(request):
    return HttpResponse("Hello, world. You're at the spotify_data index.")
