import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load product data
df = pd.read_csv('data/products.csv')

# Create TF-IDF matrix
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['product_name'])

# Compute cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

# Save model and data
with open('model/recommender.pkl', 'wb') as f:
    pickle.dump((df, similarity_matrix), f)

print("Model saved to model/recommender.pkl")
