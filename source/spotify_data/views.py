import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render
from spotify_data.models import SpotifyData
from spotify_data.forms import (DateRangeForm,
                                Artist1Form,
                                Title1Form,
                                ChartForm,
                                RegionForm
)
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

        ch_region = SpotifyData.objects.values("region").order_by("region").distinct()
        ch_chart = SpotifyData.objects.values("chart").order_by("chart").distinct()
        ch_artist = SpotifyData.objects.values("artist").order_by("artist").distinct()

        start = self.request.GET.get("FROM")
        end = self.request.GET.get("TO")
        title = self.request.GET.get("TITLE")

        data_filtered = SpotifyData.objects.filter(date__range=(start, end), artist = ch_artist[0], 
                            title=title, region=ch_region[0], chart=ch_chart[0]).values()
       
        data = data_filtered.values_list("date", "rank")
       
        fig = make_song_rank_changes_chart(data, start, end, ch_artist, title)

        chart = fig.to_html()

        context = {"chart": chart,
                "daterange_form": DateRangeForm(),
                "artist1_form": Artist1Form(),
                "title1_form": Title1Form(),
                "ch_region": ch_region,
                "ch_chart": ch_chart,
                "ch_artist": ch_artist,
        }

        return context
