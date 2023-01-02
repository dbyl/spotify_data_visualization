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

class Dashboard(TemplateView):

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
       
        data_x = [c[0] for c in data.order_by("date")]
        data_y = [c[1] for c in data.order_by("date")]

        fig = px.line(template="plotly_dark")
        fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                           name=f"{artist} - {title}", 
                           line=dict(color="#1DB954"), showlegend=True))
        fig.update_layout(title=f"{artist} - {title} rank changes from {start} to {end}", 
        title_x=0.5,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.5,
        xanchor="right",
        x=1
        ))

        chart = fig.to_html()

        context = {"chart": chart,
                "daterange_form": DateRangeForm(),
                "artist1_form": Artist1Form(),
                "title1_form": Title1Form(),
                "chart_form": ChartForm(),
                "region_form": RegionForm(),
                "reg": reg,
    
        }

        return context
