import plotly.express as px
from django.http import HttpResponse
from django.shortcuts import render
from spotify_data.models import SpotifyData
from typing import Any, Dict

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView



#def home(request):
#    return render(request, 'base.html')

class HomeView(ListView):

    model = SpotifyData
    context_object_name = "record"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["records_all"] = SpotifyData.objects.all().count()

        return context

#class Dashboard(TemplateView):

#    template_name = 'dashboard.html'

