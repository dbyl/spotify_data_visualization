from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from spotify_data import views


from spotify_data.views import (
    HomeView,
    SongRankChangesChart,
    spotifydata_create_view,
    spotifydata_update_view,
    load_titles,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("songrankchart/", SongRankChangesChart.as_view(template_name="song_rank_changes_chart.html"), \
    name="song_rank_changes_chart"),
    path('add/', views.spotifydata_create_view, name='spotifydata'),
    path('<int:pk>/', views.spotifydata_update_view, name='spotifydata_change'),
    path('ajax/load-titles/', views.load_titles, name='ajax_load_titles'),
]
