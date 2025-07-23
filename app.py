import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def load_data(filepath):
    """Loads the Netflix dataset."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Cleans the dataset by handling missing values and correcting data types."""
    # Fill missing values for specific columns
    df['country'] = df['country'].fillna(df['country'].mode()[0])
    df['cast'] = df['cast'].fillna('No Cast')
    df['director'] = df['director'].fillna('No Director')

    # Drop rows with missing 'date_added' or 'rating'
    df.dropna(subset=['date_added', 'rating'], inplace=True)

    # Convert 'duration' to numeric (minutes for movies, seasons for TV shows)
    df['duration_numeric'] = df['duration'].apply(
        lambda x: int(x.split()[0]) if 'min' in x else int(x.split()[0])
    )
    df['duration_unit'] = df['duration'].apply(
        lambda x: 'min' if 'min' in x else 'season'
    )
    return df

def feature_engineer(df):
    """Engineers features for clustering."""
    # Use MultiLabelBinarizer for 'listed_in' (genres)
    mlb = MultiLabelBinarizer()
    genres = df['listed_in'].str.split(', ')
    genre_features = pd.DataFrame(mlb.fit_transform(genres), columns=mlb.classes_, index=df.index)

    # One-hot encode 'type' and 'rating'
    type_features = pd.get_dummies(df['type'], prefix='type')
    rating_features = pd.get_dummies(df['rating'], prefix='rating')

    # Combine all features
    features_df = pd.concat([
        genre_features,
        type_features,
        rating_features,
        df['duration_numeric']
    ], axis=1)

    return features_df

def scale_features(features_df):
    """Scales the numerical features."""
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_df)
    return scaled_features

def perform_clustering(scaled_features, n_clusters=10):
    """Performs K-Means clustering."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_features)
    return clusters

def get_clustered_data(filepath='data/netflix_titles.csv'):
    """
    Main function to run the full pipeline: load, clean, engineer, and cluster.
    Returns the original dataframe with an added 'cluster' column.
    """
    # Load and clean data
    netflix_df = load_data(filepath)
    cleaned_df = clean_data(netflix_df)

    # Feature engineering and scaling
    features = feature_engineer(cleaned_df)
    scaled_features = scale_features(features)

    # Perform clustering
    clusters = perform_clustering(scaled_features, n_clusters=12) # Using 12 clusters

    # Add cluster labels to the cleaned dataframe
    clustered_df = cleaned_df.copy()
    clustered_df['cluster'] = clusters

    return clustered_df

if __name__ == '__main__':
    # This allows the script to be run directly to process and save the data
    final_data = get_clustered_data()
    # Save the result to a new CSV for the app to use
    final_data.to_csv('data/netflix_clustered.csv', index=False)
    print("Clustering complete. Data saved to 'data/netflix_clustered.csv'")