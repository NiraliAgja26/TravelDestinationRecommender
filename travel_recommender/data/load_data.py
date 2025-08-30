import os
import sys
import django
import pandas as pd

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_recommender.settings')
django.setup()

from destinations.models import Destination

def load_destinations_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    # Clear existing data (optional)
    # Destination.objects.all().delete()
    
    for _, row in df.iterrows():
        Destination.objects.create(
            name=row['name'],
            country=row['country'],
            description=row['description'],
            category=row['category'],
            best_season=row['best_season'],
            budget=row['budget'],
            activities=row['activities'],
            rating=row['rating'],
            image_url=row.get('image_url', '')
        )
    
    print(f"Successfully loaded {len(df)} destinations")

if __name__ == '__main__':
    csv_file = os.path.join(os.path.dirname(__file__), 'destinations.csv')
    if os.path.exists(csv_file):
        load_destinations_from_csv(csv_file)
    else:
        print(f"Error: CSV file not found at {csv_file}")