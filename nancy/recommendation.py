# nancy/recommendation.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie

class MovieRecommender:
    def __init__(self):
        self.movies = Movie.objects.all()
        self.df = pd.DataFrame(list(self.movies.values()))
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.df['genres'] = self.df['genres'].fillna('')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['genres'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.df.index, index=self.df['movie_title']).drop_duplicates()

    def get_recommendations(self, title, top=5):
        if title not in self.indices:
            return []
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top+1]
        movie_indices = [i[0] for i in sim_scores]
        return self.df['movie_title'].iloc[movie_indices].tolist()
