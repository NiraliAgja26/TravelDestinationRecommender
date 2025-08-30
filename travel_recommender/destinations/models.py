from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('BEACH', 'Beach'),
        ('MOUNTAIN', 'Mountain'),
        ('HISTORICAL', 'Historical'),
        ('ADVENTURE', 'Adventure'),
        ('WILDLIFE', 'Wildlife'),
        ('CULTURAL', 'Cultural'),
        ('FOOD', 'Food & Wine'),
        ('RELAX', 'Relaxation'),
    ]
    
    BUDGET_CHOICES = [
        ('CHEAP', 'Budget ($)'),
        ('MODERATE', 'Moderate ($$)'),
        ('LUXURY', 'Luxury ($$$)'),
    ]
    
    SEASON_CHOICES = [
        ('WINTER', 'Winter'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('AUTUMN', 'Autumn'),
        ('ALL', 'All Year'),
    ]
    
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    best_season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    activities = models.TextField(help_text="Comma separated list of activities")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}, {self.country}"
    
    def get_activities_list(self):
        return [activity.strip() for activity in self.activities.split(',')]
    
    def get_image_url(self):
        if self.image_url:
            return self.image_url
        # Fallback to travel-related image
        return "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.destination.name}"

class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'destination')
    
    def __str__(self):
        return f"{self.user.username}'s favorite: {self.destination.name}"