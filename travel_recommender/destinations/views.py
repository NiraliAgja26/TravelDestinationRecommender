from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Destination, Review, UserFavorite
from django.http import JsonResponse
from .forms import ReviewForm, DestinationSearchForm, PreferenceForm, WeatherSearchForm
from .weather import get_weather_data
from .recommender import get_recommendations

def home(request):
    featured_destinations = Destination.objects.order_by('-rating')[:6]
    return render(request, 'destinations/home.html', {
        'featured_destinations': featured_destinations
    })

def destination_list(request):
    destinations = Destination.objects.all()
    form = DestinationSearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        budget = form.cleaned_data.get('budget')
        
        if query:
            destinations = destinations.filter(
                Q(name__icontains=query) | 
                Q(country__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category:
            destinations = destinations.filter(category=category)
        
        if budget:
            destinations = destinations.filter(budget=budget)
    
    return render(request, 'destinations/list.html', {
        'destinations': destinations,
        'form': form
    })

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    reviews = destination.reviews.all().order_by('-created_at')
    
    # Fetch weather information
    weather_info = get_weather_data(destination.name, destination.country)
    
    # Find similar destinations based on category
    similar_destinations = Destination.objects.filter(
        category=destination.category
    ).exclude(pk=pk)[:5]
    
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = UserFavorite.objects.filter(
            user=request.user,
            destination=destination
        ).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            
            # Update destination rating efficiently
            new_rating = destination.reviews.aggregate(Avg('rating'))['rating__avg']
            if new_rating is not None:
                destination.rating = new_rating
                destination.save()
            
            messages.success(request, 'Your review has been added!')
            return redirect('destinations:detail', pk=destination.pk)
    else:
        review_form = ReviewForm()
    
    return render(request, 'destinations/detail.html', {
        'destination': destination,
        'reviews': reviews,
        'review_form': review_form,
        'is_favorite': is_favorite,
        'weather_info': weather_info,
        'similar_destinations': similar_destinations,
    })

@login_required
def toggle_favorite(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    
    favorite = UserFavorite.objects.filter(user=request.user, destination=destination).first()
    
    if favorite:
        favorite.delete()
        is_favorite = False
        message_text = f'Removed {destination.name} from favorites'
    else:
        UserFavorite.objects.create(user=request.user, destination=destination)
        is_favorite = True
        message_text = f'Added {destination.name} to favorites'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})
    
    messages.success(request, message_text)
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('destinations:detail', pk=destination.pk)

def get_recommendations_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preferences = {
                'season': form.cleaned_data.get('season'),
                'budget': form.cleaned_data.get('budget'),
                'activities': form.cleaned_data.get('activities'),
                'category': form.cleaned_data.get('category'),
                'min_rating': form.cleaned_data.get('min_rating'),
            }
            
            recommendations = get_recommendations(preferences)
            return render(request, 'destinations/recommendations.html', {
                'recommendations': recommendations,
                'preferences': preferences
            })
    else:
        form = PreferenceForm()
    
    return render(request, 'destinations/recommend.html', {'form': form})

@login_required
def user_favorites(request):
    favorites = UserFavorite.objects.filter(user=request.user).select_related('destination')
    return render(request, 'destinations/favorites.html', {'favorites': favorites})


def get_weather_view(request):
    weather_info = None
    error_message = None
    form = WeatherSearchForm(request.GET or None)

    if form.is_valid():
        city = form.cleaned_data.get('city')
        country = form.cleaned_data.get('country')
        
        weather_data = get_weather_data(city, country)
        
        if weather_data and not weather_data.get('error'):
            weather_info = weather_data
        else:
            error_message = f"Could not retrieve weather for '{city}'. Please check the city name and try again."

    return render(request, 'destinations/weather.html', {
        'form': form, 
        'weather_info': weather_info, 
        'error_message': error_message
    })