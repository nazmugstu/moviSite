from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(default=2023)
    release_date = models.DateField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    imdb_rating = models.FloatField(null=True, blank=True)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    poster_url = models.URLField(max_length=1000, null=True, blank=True)  # ৫০০ ক্যারেক্টার
    popularity = models.IntegerField(default=0)
    download_link = models.URLField(null=True, blank=True)
    streaming_link = models.URLField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_movies', blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # অথবা FloatField
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"