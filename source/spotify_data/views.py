import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData
from spotify_data.forms import DateForm
from spotify_data.forms import CharFieldForm


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
        
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get("start")
        end_date = self.request.GET.get("end")
        choosen_artist = self.request.GET.get("artist")
        choosen_title = self.request.GET.get("title")

        choosen_region = "United States"
        choosen_chart = "top200"

        context_filtered = SpotifyData.objects.filter(date__range=(start_date, end_date), artist = choosen_artist, 
                            title=choosen_title, region=choosen_region, chart=choosen_chart).values()
       
        data = context_filtered.values_list("date", "rank")
       
        data_x = [c[0] for c in data.order_by("date")]
        data_y = [c[1] for c in data.order_by("date")]

        fig = px.line(template="plotly_dark")
        fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                           name=f"{choosen_artist} - {choosen_title}", 
                           line=dict(color="#1DB954"), showlegend=True))
        fig.update_layout(title=f"{choosen_artist} - {choosen_title} rank changes from {start_date} to {end_date}", 
        title_x=0.5,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.5,
        xanchor="right",
        x=1
        ))

        chart = fig.to_html()
        context["chart"] = chart
        context["filtered"] = data
        context["form"] = DateForm()
        context["form_char"] = CharFieldForm()
        return context
