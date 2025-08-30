from django.urls import path
from . import views

app_name = 'destinations'  # If you use namespacing

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('recommendations/', views.get_recommendations_view, name='get_recommendations'),
    path('favorites/', views.user_favorites, name='user_favorites'),
    path('<int:pk>/', views.destination_detail, name='detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('weather/', views.get_weather_view, name='get_weather'),
]