import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


from django.http.response import HttpResponse
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
                                 make_song_rank_changes_comparison_chart,
                                 make_popularity_chart,
                                 make_popularity_comparison_chart,
)
from spotify_data.forms import (
                                RankChartForm,
                                RankChart2Form,
                                PopularityChartForm,
                                PopularityChartForm2,
                                ArtistMapPopularityForm
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

class RankChart(TemplateView):

    model = SpotifyData
    context_object_name = "rank_changes"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")
        s_title = self.request.GET.get("title")

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        title_id = Title.objects.filter(name=s_title, artist_id=artist_id).values_list("id", flat=True).first()
        region_id = s_region
        chart_id = s_chart

        data_filtered = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id, title = title_id
                       , region=region_id, chart=chart_id).values()
       
        data = data_filtered.values_list("date", "rank")
       
        fig = make_song_rank_changes_chart(data, s_artist, s_title)

        chart = fig.to_html()

        context = {"chart": chart,
                "rank_chart_form": RankChartForm(),     
        }

        return context

class RankChart2(TemplateView):

    model = SpotifyData
    context_object_name = "rank_changes_comparison"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")
        s_title = self.request.GET.get("title")
        s_artist_2 = self.request.GET.get("artist_2")
        s_title_2 = self.request.GET.get("title_2")

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        title_id = Title.objects.filter(name=s_title, artist_id=artist_id).values_list("id", flat=True).first()

        artist_id_2 = Artist.objects.filter(name=s_artist_2).values_list("id", flat=True).first()
        title_id_2 = Title.objects.filter(name=s_title_2, artist_id=artist_id_2).values_list("id", flat=True).first()

        region_id = s_region
        chart_id = s_chart

        data_filtered = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id, title = title_id
                       , region=region_id, chart=chart_id).values()
        
        data_filtered_2 = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id_2, title = title_id_2
                       , region=region_id, chart=chart_id).values()


       
        data = data_filtered.values_list("date", "rank")
        data_2 = data_filtered_2.values_list("date", "rank")

        data_x = [c[0] for c in data.order_by("date")]
        data_y = [c[1] for c in data.order_by("date")]
       
        fig = make_song_rank_changes_comparison_chart(data, data_2, s_artist, s_title, s_artist_2, s_title_2)

        chart = fig.to_html()

        context = {"chart": chart,
                "rank_chart_2_form": RankChart2Form(),
                "x": data_x,
                "y": data_y

        }

        return context

class PopularityChart(TemplateView):

    model = SpotifyData
    context_object_name = "popularity"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")
        s_rank = self.request.GET.get("top_rank")

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        region_id = s_region
        chart_id = s_chart

        data_filtered = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id,
                 region=region_id, chart=chart_id).values()
       
        data = data_filtered.values_list("title", "rank")

        titles_id = [x[0] for x in data if x[1] <= int(s_rank)]
        titles = [Title.objects.filter(id=x).values_list("name", flat=True).first() for x in titles_id]
       
        fig = make_popularity_chart(titles, s_artist)

        chart = fig.to_html()

        context = {"chart": chart,
                   "popularity_chart_form": PopularityChartForm()}

        return context


class PopularityChart2(TemplateView):

    model = SpotifyData
    context_object_name = "popularity_comparison"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")
        s_artist_2 = self.request.GET.get("artist_2")
        s_rank = self.request.GET.get("top_rank")

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        artist_id_2 = Artist.objects.filter(name=s_artist_2).values_list("id", flat=True).first()
        region_id = s_region
        chart_id = s_chart

        data_filtered = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id,
                 region=region_id, chart=chart_id).values()
        data_filtered_2 = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id_2,
                 region=region_id, chart=chart_id).values()
       
        data = data_filtered.values_list("title", "rank")
        data_2 = data_filtered_2.values_list("title", "rank")

        titles_id = [x[0] for x in data if x[1] <= int(s_rank)]
        titles = [Title.objects.filter(id=x).values_list("name", flat=True).first() for x in titles_id]

        titles_id_2 = [x[0] for x in data_2 if x[1] <= int(s_rank)]
        titles_2 = [Title.objects.filter(id=x).values_list("name", flat=True).first() for x in titles_id_2]
       
        fig = make_popularity_comparison_chart(titles, titles_2, s_artist, s_artist_2)

        chart = fig.to_html()

        context = {"chart": chart,
                   "popularity_chart_form_2": PopularityChartForm2()}

        return context

class ArtistMapPopularity(TemplateView):

    model = SpotifyData
    context_object_name = "artist_map_popularity"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        chart_id = s_chart

        data_filtered = SpotifyData.objects.filter(date__range=(s_start, s_end), artist = artist_id,
                 chart=chart_id).values()
       
        data = data_filtered.values_list("artist", "region", "streams")
        data 

        #titles_id = [x[0] for x in data]
        #titles = [Title.objects.filter(id=x).values_list("name", flat=True).first() for x in titles_id]
       
        #fig = make_popularity_chart(titles, s_artist)

        #chart = fig.to_html()

        context = {#"chart": chart,
                    "d":data,
                   "artist_map_popularity_form": ArtistMapPopularityForm()}

        return context



'''def autocomplete_artist(request):
    if 'term' in request.GET:
        qs = Artist.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for art in qs:
            names.append(art.name)
        # titles = [product.title for product in qs]
        return JsonResponse(names, safe=False)
    
    return render(request, 'index2.html')

def autocomplete_title(request):
    if 'term' in request.GET:
        qt = Title.objects.filter(name__icontains=request.GET.get('term'))
        names_t = list()
        for tit in qt:
            names_t.append(tit.name)
        # titles = [product.title for product in qs]
        return JsonResponse(names_t, safe=False)
        
    return render(request, 'index2.html')

def autocomplete_region(request):
    if 'term' in request.GET:
        qr = Region.objects.filter(name__icontains=request.GET.get('term'))
        names_r = list()
        for reg in qr:
            names_r.append(reg.name)
        # titles = [product.title for product in qs]
        return JsonResponse(names_r, safe=False)

    return render(request, 'index2.html')
'''


