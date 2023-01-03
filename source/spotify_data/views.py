import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render
from spotify_data.models import SpotifyData
from spotify_data.charts import (make_song_rank_changes_chart,
)

from typing import Any, Dict
from django.views.generic import TemplateView
from django.views.generic.list import ListView

class HomeView(ListView):

    model = SpotifyData
    context_object_name = "record"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["records_all"] = SpotifyData.objects.all().count()

        return context

class SongRankChangesChart(TemplateView):

    model = SpotifyData
    context_object_name = "rank_changes"
    
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        ch_start = SpotifyData.objects.values("date")
        end = '2020-01-01'
        ch_region = SpotifyData.objects.values("region").order_by("region").distinct()
        ch_chart = SpotifyData.objects.values("chart").order_by("chart").distinct()
        ch_artist = SpotifyData.objects.values("artist").order_by("artist").distinct()
        ch_title = SpotifyData.objects.values("title").order_by("title").distinct()

        data_filtered = SpotifyData.objects.filter(date__range=(ch_start, end), artist = ch_artist[0], 
                            title=ch_title[0], region=ch_region[0], chart=ch_chart[0]).values()
       
        data = data_filtered.values_list("date", "rank")
       
        fig = make_song_rank_changes_chart(data, ch_start, end, ch_artist, ch_title)

        chart = fig.to_html()

        context = {"chart": chart,
                "ch_title": ch_title,
                "ch_region": ch_region,
                "ch_chart": ch_chart,
                "ch_artist": ch_artist,
                "ch_start": ch_start,
        }

        return context
