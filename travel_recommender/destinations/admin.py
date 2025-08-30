from django.contrib import admin
from .models import Destination, Review, UserFavorite

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'category', 'best_season', 'budget', 'rating')
    list_filter = ('category', 'best_season', 'budget')
    search_fields = ('name', 'country', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_url:
            return f'<img src="{obj.image_url}" style="max-height: 200px; max-width: 300px;" />'
        return "No image"
    image_preview.allow_tags = True

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'destination__name', 'comment')

class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'created_at')
    search_fields = ('user__username', 'destination__name')

admin.site.register(Destination, DestinationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)