from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    path('movie/<int:movie_id>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('movie/<int:movie_id>/remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('register/', views.register, name='register'),
    path('', views.movie_list, name='movie_list'),
    path('trending/', views.trending, name='trending'),
    path('calendar/', views.calendar, name='calendar'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
]