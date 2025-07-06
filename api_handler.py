import requests

API_KEY = "YOUR_API_KEY"  # Optional: Get from http://www.omdbapi.com/apikey.aspx

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error": "Could not fetch data"}
