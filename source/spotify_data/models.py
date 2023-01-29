from django.db import models

class Region(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Rank(models.Model):

    name = models.IntegerField()

    def __str__(self):
        return self.name

class Chart(models.Model):

    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Artist(models.Model):

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Title(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.artist} - {self.name}"
    

class SpotifyData(models.Model):

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
    streams = models.IntegerField()

    def __str__(self):
        return str(self.title) + ", " + str(self.date) + ", " + str(self.artist) \
            + ", " + str(self.region) + ", " + str(self.chart) + ", " + str(self.streams) 
 
    



