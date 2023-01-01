from django.db import models

class SpotifyData(models.Model):

    title = models.CharField(max_length=60)
    rank = models.IntegerField()
    date = models.DateField()
    artist = models.CharField(max_length=60)
    region = models.CharField(max_length=20)
    chart = models.CharField(max_length=8)
    streams = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['rank']),
            models.Index(fields=['date']),
            models.Index(fields=['artist']),
            models.Index(fields=['region']),
            models.Index(fields=['chart']),
            ]