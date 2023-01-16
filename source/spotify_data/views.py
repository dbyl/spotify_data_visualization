import plotly.express as px
import plotly.graph_objects as go
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from spotify_data.models import (Region,
                                 Rank,
                                 Chart,
                                 Artist,
                                 Title,
                                 SpotifyData,
                                 )
                                
from spotify_data.charts import (make_song_rank_changes_chart,
)
from spotify_data.forms import (DateRangeForm,
                                Artist1Form,
                                Title1Form,
                                ChartForm,
                                RegionForm,
                                Artist1Form,
                                ArtistTitleForm,

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
        artist = self.request.GET.get("ARTISTG")
        title = self.request.GET.get("TITLE")
        region = self.request.GET.get("REGION")
        chart = self.request.GET.get("CHART")
        


        chart_id = Chart.objects.filter(name=chart["name"]).values("id")

        data_filtered = SpotifyData.objects.filter(date__range=(start, end), artist = artist, title = title
                            , region=region, chart=chart_id).values()
       
        data = data_filtered.values_list("date", "rank")
       
        fig = make_song_rank_changes_chart(data, start, end, artist, title)

        chart = fig.to_html()


        context = {"chart": chart,
                "daterange_form": DateRangeForm(),
                "artist1_form": Artist1Form(),
                "title1_form": Title1Form(),
                "chart_form": ChartForm(),
                "region_form": RegionForm(),
                "region_form":RegionForm(),  
                "df":data_filtered             
        }

        return context

def spotifydata_create_view(request):
    form = ArtistTitleForm()
    if request.method == 'GET':
        form = ArtistTitleForm(request.GET)
        if form.is_valid():
            form.save()
            return redirect('spotifydata')
    return render(request, 'spotifydatas/home1.html', {'form': form})


def spotifydata_update_view(request, pk):
    spotifydata = get_object_or_404(SpotifyData, pk=pk)
    form = ArtistTitleForm(instance=spotifydata)
    if request.method == 'GET':
        form = ArtistTitleForm(request.GET, instance=spotifydata)
        if form.is_valid():
            form.save()
            return redirect('spotifydata_change', pk=pk)
    return render(request, 'spotifydatas/home1.html', {'form': form})

def load_titles(request):
    artist_id = request.GET.get('artist_id')
    titles = Title.objects.filter(artist_id=artist_id).all()
    return render(request, 'spotifydatas/title_dropdown_list_options.html', {'titles': titles})



