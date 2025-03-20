from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from movie_app.models import Review, Favorite

@login_required
def user_profile(request):
    reviews = Review.objects.filter(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'user_auth/profile.html', {'reviews': reviews, 'favorites': favorites})