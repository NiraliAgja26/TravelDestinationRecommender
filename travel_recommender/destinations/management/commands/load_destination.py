from django.core.management.base import BaseCommand
import pandas as pd
from destinations.models import Destination

class Command(BaseCommand):
    help = 'Load destinations from CSV'

    def handle(self, *args, **options):
        csv_file = 'data/destinations.csv'
        
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                Destination.objects.create(
                    name=row['name'],
                    country=row['country'],
                    description=row['description'],
                    category=row['category'],
                    best_season=row['best_season'],
                    budget=row['budget'],
                    activities=row['activities'],
                    rating=row['rating']
                )
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(df)} destinations'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))