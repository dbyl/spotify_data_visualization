from django.db import models

class SpotifyData(models.Model):
    
        title = models.CharField(max_length=200)
        rank = models.DecimalField(max_digits=5, decimal_places=0)
        date =  models.DateField()
        artist = models.CharField(max_length=200)
        url = models.CharField(max_length=200)
        region = models.CharField(max_length=50)
        chart = models.CharField(max_length=15)
        streams = models.DecimalField(max_digits=50, decimal_places=0)
        
