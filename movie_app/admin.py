from django.contrib import admin
from .models import Genre, Movie, Review, Favorite

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'imdb_rating', 'poster', 'poster_url')
    filter_horizontal = ('genres',)

admin.site.register(Genre)
admin.site.register(Movie,MovieAdmin)
admin.site.register(Review)
admin.site.register(Favorite)