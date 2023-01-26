from django.db.models import Sum
from spotify_data.models import (Region,
                                 Artist,
                                 Title,
                                 SpotifyData,
                                 )
                                
from spotify_data.charts import (make_song_rank_changes_chart,
                                 make_song_rank_changes_comparison_chart,
                                 make_popularity_chart,
                                 make_popularity_comparison_chart,
                                 make_artist_popularity_map,
                                 make_song_popularity_map,
                                 make_top_streamed_artist_chart,
                                 make_top_streamed_artist_comparison_chart,
                                 make_top_streamed_song_chart,
                                 make_top_streamed_song_comparison_chart
)

from spotify_data.forms import (
                                RankChartForm,
                                RankChart2Form,
                                PopularityChartForm,
                                PopularityChartForm2,
                                ArtistMapPopularityForm,
                                SongMapPopularityForm,
                                TopStreamedArtistsForm,
                                TopStreamedArtistsForm2,
                                TopStreamedSongsForm,
                                TopStreamedSongsForm2,

)

from spotify_data.constants import (
                                REGIONS_ID_ISO,
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
        chart_id = s_chart

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()

        data_filtered_artist = list(SpotifyData.objects.filter(date__range=(s_start, s_end)\
                ,artist = artist_id, chart=chart_id).values_list("region")\
                .annotate(streams=Sum("streams")).exclude(region=23).order_by("region"))

        data_filtered_all_artist = list(SpotifyData.objects.filter(date__range=(s_start, s_end)\
                ,chart=chart_id).values_list("region").annotate(streams=Sum("streams"))\
                .exclude(region=23).order_by("region"))

        regions_id = [x[0] for x in data_filtered_artist]
        regions_iso = [REGIONS_ID_ISO[x] for x in regions_id]
        regions_name = [Region.objects.filter(id=x).values_list("name", flat=True)\
                    .exclude(name='Global').first() for x in regions_id\
                     if Region.objects.filter(id=x).values_list("name", flat=True)\
                    .exclude(name='Global').first() is not None]
        share_in_all_streams = []

        for i, j  in zip(data_filtered_artist, data_filtered_all_artist):
            for j in data_filtered_all_artist:
                if i[0] == j[0]:
                    if i[1] == 0 or j[1] == 0:
                        share_in_all_streams.append(0)
                    else:
                        share_in_all_streams.append(i[1]/j[1]*100)
                       
        fig = make_artist_popularity_map(s_artist, regions_iso, regions_name, share_in_all_streams)

        choropleth = fig.to_html()

        context = { "choropleth": choropleth,
                   "artist_map_popularity_form": ArtistMapPopularityForm()}

        return context
    
class SongMapPopularity(TemplateView):

    model = SpotifyData
    context_object_name = "song_map_popularity"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_chart = self.request.GET.get("chart")
        s_artist = self.request.GET.get("artist")
        s_title = self.request.GET.get("title")
        chart_id = s_chart

        artist_id = Artist.objects.filter(name=s_artist).values_list("id", flat=True).first()
        title_id = Title.objects.filter(name=s_title, artist=artist_id).values_list("id", flat=True).first()

        data_filtered_songs = list(SpotifyData.objects.filter(date__range=(s_start, s_end)\
                ,artist = artist_id, title = title_id, chart=chart_id).values_list("region")\
                .annotate(streams=Sum("streams")).exclude(region=23).order_by("region"))

        data_filtered_all_artist = list(SpotifyData.objects.filter(date__range=(s_start, s_end)\
                ,chart=chart_id).values_list("region").annotate(streams=Sum("streams"))\
                .exclude(region=23).order_by("region"))

        regions_id = [x[0] for x in data_filtered_songs]
        regions_iso = [REGIONS_ID_ISO[x] for x in regions_id]
        regions_name = [Region.objects.filter(id=x).values_list("name", flat=True)\
                    .exclude(name='Global').first() for x in regions_id\
                     if Region.objects.filter(id=x).values_list("name", flat=True)\
                    .exclude(name='Global').first() is not None]
        share_in_all_streams = []

        for i, j  in zip(data_filtered_songs, data_filtered_all_artist):
            for j in data_filtered_all_artist:
                if i[0] == j[0]:
                    if i[1] == 0 or j[1] == 0:
                        share_in_all_streams.append(0)
                    else:
                        share_in_all_streams.append(i[1]/j[1]*100)
                       
        fig = make_song_popularity_map(s_artist, s_title, regions_iso, regions_name, share_in_all_streams)

        choropleth = fig.to_html()

        context = {"choropleth": choropleth,
                   "song_map_popularity_form": SongMapPopularityForm()}

        return context

class TopStreamedArtistsChart(TemplateView):

    model = SpotifyData
    context_object_name = "top_streamed_artists"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_chart = self.request.GET.get("chart")
        s_top_streamed = self.request.GET.get("top_streamed")
        region_id = s_region
        chart_id = s_chart

        region_name = Region.objects.filter(id=region_id).values_list("name", flat=True).first()

        if s_top_streamed is None:
            s_top_streamed = 20 #any int

        data_filtered = list(SpotifyData.objects.filter(date__range=(s_start, s_end),
                 region=region_id, chart=chart_id).values_list("artist").annotate(streams=Sum("streams"))\
                .order_by('-streams'))[:int(s_top_streamed)]
                
        artists_id = [x[0] for x in data_filtered]
        artists_name = [Artist.objects.filter(id=x).values_list("name", flat=True)\
                    .first() for x in artists_id]
        artist_streams = [x[1] for x in data_filtered]
    
        fig = make_top_streamed_artist_chart(artist_streams, artists_name, region_name)

        chart = fig.to_html()

        context = {"chart": chart,
                   "top_streamed_artists_form": TopStreamedArtistsForm()}

        return context

class TopStreamedArtistsChart2(TemplateView):

    model = SpotifyData
    context_object_name = "top_streamed_artists"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        
        context = super().get_context_data(**kwargs)

        s_start = self.request.GET.get("start")
        s_end = self.request.GET.get("end")
        s_region = self.request.GET.get("region")
        s_region_2 = self.request.GET.get("region_2")
        s_chart = self.request.GET.get("chart")
        s_top_streamed = self.request.GET.get("top_streamed")
        region_id = s_region
        region_id_2 = s_region_2
        chart_id = s_chart

        region_name = Region.objects.filter(id=region_id).values_list("name", flat=True).first()
        region_name_2 = Region.objects.filter(id=region_id_2).values_list("name", flat=True).first()

        if s_top_streamed is None:
            s_top_streamed = 10 #any int

        data_filtered = list(SpotifyData.objects.filter(date__range=(s_start, s_end),
                 region=region_id, chart=chart_id).values_list("artist").annotate(streams=Sum("streams"))\
                .order_by('-streams'))[:int(s_top_streamed)]

        data_filtered_2 = list(SpotifyData.objects.filter(date__range=(s_start, s_end),
                 region=region_id_2, chart=chart_id).values_list("artist").annotate(streams=Sum("streams"))\
                .order_by('-streams'))[:int(s_top_streamed)]
                
        artists_id = [x[0] for x in data_filtered]
        artists_name = [Artist.objects.filter(id=x).values_list("name", flat=True)\
                    .first() for x in artists_id]
        artist_streams = [x[1] for x in data_filtered]

        artists_id_2 = [x[0] for x in data_filtered_2]
        artists_name_2 = [Artist.objects.filter(id=x).values_list("name", flat=True)\
                    .first() for x in artists_id_2]
        artist_streams_2 = [x[1] for x in data_filtered_2]
    
        fig = make_top_streamed_artist_comparison_chart(artist_streams, artists_name, region_name,
                                             artist_streams_2, artists_name_2, region_name_2)

        chart = fig.to_html()

        context = {"chart": chart,
                   "top_streamed_artists_form_2": TopStreamedArtistsForm2()}

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


