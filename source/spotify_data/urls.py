from django.urls import path

from spotify_data.views import (
    HomeView,
    Dashboard,
)

urlpatterns = [
    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("dashboard/", Dashboard.as_view(template_name="dashboard.html"), name="dashboard")
]
