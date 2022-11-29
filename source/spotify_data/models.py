from django.db import models


class SpotifyData(models.Model):

    title = models.CharField(max_length=200)
    rank = models.IntegerField()
    date = models.DateField()
    artist = models.CharField(max_length=200)
    region = models.CharField(max_length=50)
    chart = models.CharField(max_length=15)
    streams = models.IntegerField()
