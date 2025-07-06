import requests

API_KEY = 'b0e08b032e510d4fd706d637d2c6216c'  # 🔁 Replace with your TMDb API key

def get_movie_info(movie_title):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(search_url)
        data = response.json()

        if data['results']:
            movie = data['results'][0]
            poster_path = movie.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            rating = movie.get('vote_average', 'N/A')
            overview = movie.get('overview', '')
            movie_id = movie.get('id')

            # Get genre
            genre_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            genre_resp = requests.get(genre_url).json()
            genres = [g['name'] for g in genre_resp.get('genres', [])]
            genre_text = ", ".join(genres) if genres else "N/A"

            return {
                "poster_url": poster_url,
                "rating": rating,
                "overview": overview,
                "genres": genre_text,
                "youtube_search": f"https://www.youtube.com/results?search_query={movie_title.replace(' ', '+')}+trailer"
            }

    except Exception as e:
        print("TMDb API Error:", e)
        return {}

    return {}
