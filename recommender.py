import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(title, df):
    # 🔁 Combine title, genre, and description for richer features
    df['combined_text'] = df['title'] + " " + df['genre'] + " " + df['description']
    
    # 🧠 Convert text to TF-IDF vectors
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_text'])

    # 📐 Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 🔍 Get index of the given movie title
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    idx = indices.get(title)

    if idx is None:
        return ["Movie not found!"]

    # 🎯 Get top 5 similar movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]

    return df['title'].iloc[movie_indices].tolist()
