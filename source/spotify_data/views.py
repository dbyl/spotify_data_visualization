import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData
from typing import Any, Dict

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView



class HomeView(ListView):

    model = SpotifyData
    context_object_name = "record"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["records_all"] = SpotifyData.objects.all().count()

        return context

class Dashboard(TemplateView):

    model = SpotifyData
    context_object_name = "rank_changes"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        #date = SpotifyData.objects.filter(date__range=("2019-02-05", "2019-09-05"))
        #artist = SpotifyData.objects.filter(artist="Billy Eilish")
        #title = SpotifyData.objects.filter(title="bad guy")

        #chart = SpotifyData.objects.filter(chart="top200")

        context = super().get_context_data(**kwargs)
        context_filtered = SpotifyData.objects.filter(date__range=("2019-02-05", "2019-09-05"), artist="Billy Eilish", title="bad guy", region="United States", chart="top200")

        #x = context["rank"].values_list(date__range=("2019-02-05", "2019-09-05"), flat=True)
        #y = context["rank"].values_list("rank")

        fig_1 = px.line(template='plotly_dark')
        fig_1.add_trace(go.Scatter(x=[c["date"] for c in context_filtered[1]], y=[c["rank"] for c in context_filtered], 
                           name=f'Name', line=dict(color="#1DB954"), showlegend=True))
        fig_1.update_layout(title="Ranking", 
        title_x=0.5,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ))

        chart = fig_1.to_html()
        context["chart"] = chart
        context["filtered"] = context_filtered
        return context