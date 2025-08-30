import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Destination

def load_data():
    """Load destination data into a pandas DataFrame"""
    destinations = Destination.objects.all().values()
    return pd.DataFrame.from_records(destinations)

def prepare_features(df):
    """Prepare features for KNN model"""
    df['feature_text'] = df['category'] + ' ' + df['best_season'] + ' ' + df['budget'] + ' ' + df['activities']
    return df

def build_knn_model():
    """Build and return a KNN pipeline"""
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['category', 'best_season', 'budget']),
            ('text', TfidfVectorizer(max_features=100, stop_words='english'), 'feature_text')
        ])
    
    return Pipeline([
        ('preprocessor', preprocessor),
        ('scaler', StandardScaler(with_mean=False)),
        ('knn', NearestNeighbors(n_neighbors=10, metric='cosine'))
    ])

def get_recommendations(user_prefs):
    """Get recommendations based on user preferences"""
    # Get all destinations
    df = load_data()
    
    # Filter by minimum rating if specified
    min_rating = user_prefs.get('min_rating')
    if min_rating:
        df = df[df['rating'] >= float(min_rating)]
    
    if df.empty:
        return []
    
    df = prepare_features(df)
    
    # Build and fit KNN model
    model = build_knn_model()
    model.fit(df)
    
    # Create user preference data point
    user_data = {
        'category': [user_prefs['category']],
        'best_season': [user_prefs['season']],
        'budget': [user_prefs['budget']],
        'feature_text': [
            f"{user_prefs['category']} {user_prefs['season']} "
            f"{user_prefs['budget']} {user_prefs.get('activities', '')}"
        ]
    }
    user_df = pd.DataFrame(user_data)
    
    # Transform user data
    user_transformed = model.named_steps['preprocessor'].transform(user_df)
    
    # Find nearest neighbors
    distances, indices = model.named_steps['knn'].kneighbors(user_transformed)
    
    # Get recommended destinations
    recommended_indices = indices[0]
    recommended_dests = []
    
    for idx in recommended_indices:
        dest_id = df.iloc[idx]['id']
        try:
            destination = Destination.objects.get(id=dest_id)
            recommended_dests.append(destination)
        except Destination.DoesNotExist:
            continue
    
    # Sort by rating descending
    recommended_dests.sort(key=lambda x: x.rating, reverse=True)
    return recommended_dests[:8]  # Return top 8 recommendations