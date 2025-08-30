from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from destinations import views as destination_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', destination_views.home, name='home'),
    path('destinations/', include('destinations.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)