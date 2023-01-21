from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from spotify_data import views


from spotify_data.views import (
    HomeView,
    RankChart,
    RankChart2,
    PopularityChart,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("rankchart/", RankChart.as_view(template_name="rank_chart.html"), \
    name="rank_chart"),
    path("rankchart2/", RankChart2.as_view(template_name="rank_chart_2.html"), \
    name="rank_chart_2"),
    path("populrank/", PopularityChart.as_view(template_name="popularity_chart.html"), \
    name="popul_chart"),
]
