from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from spotify_data import views
from spotify_data.forms import (PassResetForm,
                                PassSetForm,
                                PassChangeForm)


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
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("login_required/", views.login_required, name="login_required"),
    path("logout/", views.logout_user, name="logout"),
    path("reset_password/", auth_views.PasswordResetView.as_view(form_class=PassResetForm, template_name="accounts/password_reset.html"), name="reset_password"),
    path("change_password/", auth_views.PasswordChangeView.as_view(form_class=PassChangeForm, template_name="accounts/password_change_form.html"), name="change_password"),
    path("change_password_complete/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change_complete.html"), name="password_change_done"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class=PassSetForm, template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_sent_complete.html"), name="password_reset_complete"),

    path("", HomeView.as_view(template_name="index.html"), name="home"),
    path("rankchart/", RankChart.as_view(template_name="charts/rank_chart.html"), \
    name="rank_chart"),
    path("rankchart2/", RankChart2.as_view(template_name="charts/rank_chart_2.html"), \
    name="rank_chart_2"),
    path("populrank/", PopularityChart.as_view(template_name="charts/popularity_chart.html"), \
    name="popul_chart"),
    path("populrank2/", PopularityChart2.as_view(template_name="charts/popularity_chart_2.html"), \
    name="popul_chart_2"),
    path("artistmappopul/", ArtistMapPopularity.as_view(template_name="charts/artist_map_popularity.html"), \
    name="artist_map_popul"),
    path("songmappopul/", SongMapPopularity.as_view(template_name="charts/song_map_popularity.html"), \
    name="song_map_popul"),
    path("topstreamedart/", TopStreamedArtistsChart.as_view(template_name="charts/top_streamed_artists_chart.html"), \
    name="top_streamed_artists_chart"),
    path("topstreamedart2/", TopStreamedArtistsChart2.as_view(template_name="charts/top_streamed_artists_chart_2.html"), \
    name="top_streamed_artists_chart_2"),
    path("topstreamedsongs/", TopStreamedSongsChart.as_view(template_name="charts/top_streamed_songs_chart.html"), \
    name="top_streamed_songs_chart"),
    path("topstreamedsongs2/", TopStreamedSongsChart2.as_view(template_name="charts/top_streamed_songs_chart_2.html"), \
    name="top_streamed_songs_chart_2"),
]
