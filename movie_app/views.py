from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomLoginForm
from .models import Movie, Review, Genre
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
import requests



def movie_list(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    query = request.GET.get('q')
    if query:
        movies = movies.filter(title__icontains=query) | movies.filter(description__icontains=query)
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movie_app/movie_list.html', {
        'movies': page_obj,
        'genres': genres,
        'query': query,
        'selected_genre': genre_id,
        'page_obj': page_obj
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_app/movie_detail.html', {'movie': movie})

def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        if comment and rating:
            Review.objects.create(movie=movie, user=request.user, comment=comment, rating=float(rating))
            return redirect('movie_detail', movie_id=movie.id)
    return render(request, 'movie_app/add_review.html', {'movie': movie})

@login_required
def add_to_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.is_authenticated:
        movie.favorites.add(request.user)
    return redirect('movie_detail', movie_id=movie.id)

@login_required
def remove_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.is_authenticated:
        movie.favorites.remove(request.user)
    return redirect('movie_detail', movie_id=movie.id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('movie_list')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def custom_logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('movie_list')
    return render(request, 'registration/logout.html')

def trending(request):
    movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:8]
    return render(request, 'movie_app/trending.html', {'movies': movies})

def calendar(request):
    movies_list = Movie.objects.order_by('release_year')
    paginator = Paginator(movies_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movie_app/calendar.html', {
        'movies': page_obj,
        'page_obj': page_obj
    })


def chatbot(request):
    if request.method == "POST":
        message = request.POST.get('message', '').lower().strip()
        api_key = '2503232ad80d9e99f4e88d075d6ea8d8'  # তোমার কী

        # ✅ শুভেচ্ছা বিনিময়
        if any(word in message for word in ["হাই", "হ্যালো", "সুপ্রভাত", "সন্ধ্যা", "কেমন আছো", "কি খবর"]):
            greetings_responses = [
                "হ্যালো! 😊 আমি মুভি বট। কিভাবে সাহায্য করতে পারি?",
                "সুপ্রভাত! আজ কোন মুভির খবর চাও?",
                "হাই! আমি এখানে আছি, বলো কী জানতে চাও।",
                "কি খবর বন্ধু? মুভির খোঁজে এসেছো?"
            ]
            import random
            return JsonResponse({'response': random.choice(greetings_responses)})

        # সাধারণ কথোপকথন
        if "তোমার নাম" in message:
            return JsonResponse({'response': "আমার নাম 'মুভি বট'। তুমি কী জানতে চাও?"})
        
        if "তোমার কাজ" in message or "তুমি কী করতে পারো" in message:
            return JsonResponse({'response': "আমি মুভি সম্পর্কিত তথ্য দিতে পারি, যেমন রেটিং, কাস্ট, রিভিউ, জনপ্রিয় মুভি, এবং আরও অনেক কিছু। জাস্ট প্রশ্ন করে দেখো!"})
        
        if "কে বানাইছে" in message or "তোমাকে কে বানিয়েছে" in message:
            return JsonResponse({'response': "আমাকে বানাইছে নাজমুল ভাই! উনি Django দিয়ে বানাইছেন আমাকে। 😄"})
        
        if "হেল্প" in message or "help" in message:
            return JsonResponse({'response': "তুমি আমাকে বলতে পারো:\n- 'জনপ্রিয় মুভি'\n- '2023 এর অ্যাকশন মুভি'\n- 'Inception এর রেটিং'\n- 'Avengers এর কাস্ট'\n- 'The Batman এর রিভিউ'\n- 'কমেডি মুভি' ইত্যাদি।"})
        
        if "ধন্যবাদ" in message or "thanks" in message:
            return JsonResponse({'response': "স্বাগতম! আরও কিছু জানতে চাও?"})
        
        if "ডাউনলোড" in message:
            return JsonResponse({'response': "দুঃখিত, আমি মুভি ডাউনলোড লিংক দিতে পারি না। তবে তুমি মুভির রেটিং, কাস্ট বা রিভিউ জানতে পারো!"})
        
        if "movie bot" in message or "মুভি বট" in message:
            return JsonResponse({'response': "আমি 'মুভি বট' — মুভি বিষয়ক চ্যাটবট। আমি তোমাকে মুভি সম্পর্কিত নানা তথ্য দিতে পারি!"})

        # মুভি নাম বের করা
        def extract_movie_name(msg):
            if "'" in msg:
                start = msg.index("'") + 1
                end = msg.index("'", start)
                return msg[start:end]
            if "এর" in msg:
                return msg.split("এর")[0].strip()
            if "কত" in msg:
                return msg.split("কত")[0].strip()
            return " ".join(msg.split()[:2])  # প্রথম দুটো শব্দ

        movie_name = extract_movie_name(message)
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

        try:
            # জনপ্রিয় মুভি
            if any(word in message for word in ["জনপ্রিয়", "জনপ্রিয়", "popular"]):
                url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page=1"
                response = requests.get(url)
                response.raise_for_status()
                movies = response.json()['results'][:3]
                movie_list = ", ".join([movie['title'] for movie in movies])
                return JsonResponse({'response': f"সর্বশেষ জনপ্রিয় মুভি: {movie_list}"})
            
            # 2023-এর অ্যাকশন মুভি
            elif any(year in message for year in ["2023", "২০২৩"]) and any(action in message for action in ["অ্যাকশন", "একশন", "action"]):
                url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_year=2023&with_genres=28&sort_by=popularity.desc"
                response = requests.get(url)
                response.raise_for_status()
                movies = response.json()['results'][:3]
                movie_list = ", ".join([movie['title'] for movie in movies])
                return JsonResponse({'response': f"2023-এর সেরা অ্যাকশন মুভি: {movie_list}"})
            
            # রেটিং
            elif "রেটিং" in message or "rating" in message:
                response = requests.get(search_url)
                response.raise_for_status()
                data = response.json()
                if data.get('results'):
                    movie = data['results'][0]
                    return JsonResponse({'response': f"'{movie['title']}'-এর রেটিং: {movie['vote_average']}"} )
            
            # কাস্ট
            elif "কাস্ট" in message or "cast" in message:
                response = requests.get(search_url)
                response.raise_for_status()
                data = response.json()
                if data.get('results'):
                    movie_id = data['results'][0]['id']
                    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
                    cast_response = requests.get(url)
                    cast_data = cast_response.json()
                    cast = [actor['name'] for actor in cast_data['cast'][:3]]
                    return JsonResponse({'response': f"'{movie_name}'-এর কাস্ট: {', '.join(cast)}"})
            
            # জেনার ভিত্তিক মুভি
            elif any(genre in message for genre in ["কমেডি", "অ্যাকশন", "হরর"]):
                genre_map = {"কমেডি": 35, "অ্যাকশন": 28, "হরর": 27}
                genre_id = next((gid for g, gid in genre_map.items() if g in message), None)
                if genre_id:
                    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&sort_by=popularity.desc"
                    response = requests.get(url)
                    response.raise_for_status()
                    movies = response.json()['results'][:3]
                    movie_list = ", ".join([movie['title'] for movie in movies])
                    genre_name = next(g for g in genre_map if g in message)
                    return JsonResponse({'response': f"কিছু {genre_name} মুভি: {movie_list}"})
            
            # রিভিউ
            elif "রিভিউ" in message or "review" in message:
                response = requests.get(search_url)
                response.raise_for_status()
                data = response.json()
                if data.get('results'):
                    movie_data = data['results'][0]
                    movie_id = movie_data['id']
                    try:
                        movie = Movie.objects.get(id=movie_id)  # TMDb ID দিয়ে ম্যাচ
                        reviews = movie.reviews.all()[:3]
                        if reviews:
                            review_list = "\n".join([f"{r.user.username}: {r.comment} (রেটিং: {r.rating})" for r in reviews])
                            return JsonResponse({'response': f"'{movie_data['title']}'-এর রিভিউ:\n{review_list}"})
                        else:
                            return JsonResponse({'response': f"'{movie_data['title']}'-এর কোনো রিভিউ নেই। TMDb থেকে সারাংশ: {movie_data['overview']}"} )
                    except Movie.DoesNotExist:
                        return JsonResponse({'response': f"'{movie_data['title']}'-এর কোনো রিভিউ নেই। TMDb থেকে সারাংশ: {movie_data['overview']}"} )

            return JsonResponse({'response': "দুঃখিত, বুঝতে পারিনি। মুভির নামটা ঠিক করে লেখো!"})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'response': "দুঃখিত, কিছু সমস্যা হয়েছে।"})

    return render(request, 'movie_app/chatbot.html')



def some_view(request):
    movies = Movie.objects.all().order_by('id')  # অথবা 'title', 'release_date' ইত্যাদি
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'template.html', {'page_obj': page_obj})