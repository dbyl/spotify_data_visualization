from django.contrib import admin

from .models import (SpotifyData,
                     Region,
                     Rank,
                     Chart,
                     Artist,
                     Title)


admin.site.register(Region)
admin.site.register(Rank)
admin.site.register(Chart)
admin.site.register(Artist)
admin.site.register(Title)
admin.site.register(SpotifyData)


