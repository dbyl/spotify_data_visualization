from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from spotify_data.views import (
    HomeView,
    SongRankChangesChart,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("songrankchart/", SongRankChangesChart.as_view(template_name="song_rank_changes_chart.html"), \
    name="song_rank_changes_chart")
]
