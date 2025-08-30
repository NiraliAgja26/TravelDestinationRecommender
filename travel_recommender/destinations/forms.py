from django import forms
from .models import Review, Destination

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'})
        }

class DestinationSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search destinations...',
            'class': 'form-control'
        })
    )
    category = forms.ChoiceField(
        choices=Destination.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    budget = forms.ChoiceField(
        choices=Destination.BUDGET_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PreferenceForm(forms.Form):
    season = forms.ChoiceField(
        choices=Destination.SEASON_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    budget = forms.ChoiceField(
        choices=Destination.BUDGET_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        choices=Destination.CATEGORY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_rating = forms.ChoiceField(
        choices=[
            ('', 'Any Rating'),
            ('3.0', '3+ Stars'),
            ('4.0', '4+ Stars'),
            ('4.5', '4.5+ Stars')
        ],
        required=False,
        label='Minimum Rating',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class WeatherSearchForm(forms.Form):
    city = forms.CharField(
        label="City",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., London'})
    )
    country = forms.CharField(
        label="Country Code (Optional)",
        max_length=5,
        required=False,
        help_text="e.g., UK, US, FR",
        widget=forms.TextInput(attrs={'placeholder': 'e.g., UK'})
    )
