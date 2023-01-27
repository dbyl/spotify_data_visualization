from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from spotify_data import views


from spotify_data.views import (
    HomeView,
    RankChart,
    RankChart2,
    PopularityChart,
    PopularityChart2,
    ArtistMapPopularity,
    SongMapPopularity,
    TopStreamedArtistsChart,
    TopStreamedArtistsChart2,
    TopStreamedSongsChart,
    TopStreamedSongsChart2,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("rankchart/", RankChart.as_view(template_name="rank_chart.html"), \
    name="rank_chart"),
    path("rankchart2/", RankChart2.as_view(template_name="rank_chart_2.html"), \
    name="rank_chart_2"),
    path("populrank/", PopularityChart.as_view(template_name="popularity_chart.html"), \
    name="popul_chart"),
    path("populrank2/", PopularityChart2.as_view(template_name="popularity_chart_2.html"), \
    name="popul_chart_2"),
    path("artistmappopul/", ArtistMapPopularity.as_view(template_name="artist_map_popularity.html"), \
    name="artist_map_popul"),
    path("songmappopul/", SongMapPopularity.as_view(template_name="song_map_popularity.html"), \
    name="song_map_popul"),
    path("topstreamedart/", TopStreamedArtistsChart.as_view(template_name="top_streamed_artists_chart.html"), \
    name="top_streamed_artists_chart"),
    path("topstreamedart2/", TopStreamedArtistsChart2.as_view(template_name="top_streamed_artists_chart_2.html"), \
    name="top_streamed_artists_chart_2"),
    path("topstreamedsongs/", TopStreamedSongsChart.as_view(template_name="top_streamed_songs_chart.html"), \
    name="top_streamed_songs_chart"),
    path("topstreamedsongs2/", TopStreamedSongsChart2.as_view(template_name="top_streamed_songs_chart_2.html"), \
    name="top_streamed_songs_chart_2"),
]
