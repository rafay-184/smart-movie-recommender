import pandas as pd

def load_movie_data(path="data/movies.csv"):
    try:
        df = pd.read_csv(path)
        df.dropna(subset=['description'], inplace=True)
        return df
    except Exception as e:
        print(f"Error loading movie data: {e}")
        return pd.DataFrame()
