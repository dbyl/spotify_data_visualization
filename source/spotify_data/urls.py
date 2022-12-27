from django.urls import path

from spotify_data.views import (
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
]
