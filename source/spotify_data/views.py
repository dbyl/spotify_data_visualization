import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render
from spotify_data.models import (Region,
                                 Rank,
                                 Chart,
                                 Artist,
                                 Title,
                                 ArtistTitle,
                                 SpotifyData)
                                
from spotify_data.charts import (make_song_rank_changes_chart,
)
from spotify_data.forms import (DateRangeForm,
                                Artist1Form,
                                Title1Form,
                                ChartForm,
                                RegionForm,
                                Artist1Form,
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

        start = self.request.GET.get("FROM")
        end = self.request.GET.get("TO")
        artist = self.request.GET.get("ARTIST")
        title = self.request.GET.get("TITLE")
        region = self.request.GET.get("REGION")
        chart = self.request.GET.get("CHART")

        data_filtered = SpotifyData.objects.filter(date__range=(start, end), artist = artist, 
                            title=title, region=region, chart=chart).values()
       
        data = data_filtered.values_list("date", "rank")
       
        fig = make_song_rank_changes_chart(data, start, end, artist, title)

        chart = fig.to_html()


        context = {"chart": chart,
                "daterange_form": DateRangeForm(),
                "artist1_form": Artist1Form(),
                "title1_form": Title1Form(),
                "chart_form": ChartForm(),
                "region_form": RegionForm(),
        }

        return context
