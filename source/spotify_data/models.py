from django.db import models


class SpotifyData(models.Model):

    title = models.CharField(max_length=60)
    rank = models.IntegerField()
    date = models.DateField()
    artist = models.CharField(max_length=60)
    region = models.CharField(max_length=20)
    chart = models.CharField(max_length=8)
    streams = models.IntegerField()
