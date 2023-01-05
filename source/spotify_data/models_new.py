from django.db import models



class Region(models.Model):

    region = models.CharField(max_length=20)

class Rank(models.Model):

    rank = models.IntegerField()

class Chart(models.Model):

    chart = models.CharField(max_length=8)

class Artist(models.Model):

    artist = models.CharField(max_length=60)

class Title(models.Model):

    title = models.CharField(max_length=60)
    
class ArtistTitle(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    title = models.ForeignKey(Title, on_delete=models.PROTECT)

class SpotifyData(models.Model):

    title = models.ForeignKey(ArtistTitle, on_delete=models.PROTECT)
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    date = models.DateField()
    artist = models.ForeignKey(ArtistTitle, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    chart = models.ForeignKey(Chart, on_delete=models.PROTECT)
    streams = models.IntegerField()

    



