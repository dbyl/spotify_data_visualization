import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData
from spotify_data.forms import DateForm
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
    
    def start_end_date(request):

        filtered_data = SpotifyData.objects.all()

        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        
        context = {'form': DateForm}
        return render(request, context)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        start_date = self.start_end_date()
        end_date = self.start_end_date()

        context_filtered = SpotifyData.objects.filter(date__range=(start_date, end_date), artist="Billie Eilish", 
                            title="bad guy", region="United States", chart="top200").values()
       
        data = context_filtered.values_list("date", "rank")
       
        data_x = [c[0] for c in data.order_by("date")]
        data_y = [c[1] for c in data.order_by("date")]

        fig = px.line(template='plotly_dark')
        fig.add_trace(go.Scatter(x=data_x, y=data_y, 
                           name=f'Name', line=dict(color="#1DB954"), showlegend=True))
        fig.update_layout(title="Ranking", 
        title_x=0.5,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
        ))

        chart = fig.to_html()
        context["chart"] = chart
        context["filtered"] = data
        context["form"] = DateForm()
        return context
