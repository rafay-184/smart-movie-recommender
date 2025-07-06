import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
from functools import partial

from data_handler import load_movie_data
from recommender import get_recommendations
from tmdb_handler import get_movie_info


df = load_movie_data()

def open_tmdb_search(movie_title):
    """Open TMDb search page for a given movie title"""
    query = movie_title.replace(" ", "+")
    url = f"https://www.themoviedb.org/search?query={query}"
    webbrowser.open_new_tab(url)

from tooltip import CreateToolTip

from tooltip import CreateToolTip

def recommend():
    title = entry.get()
    if not title:
        messagebox.showerror("Input Error", "Please enter a movie title.")
        return

    recommendations = get_recommendations(title, df)
    output.delete(0, tk.END)

    for widget in poster_frame.winfo_children():
        widget.destroy()

    for movie in recommendations:
        output.insert(tk.END, movie)

        info = get_movie_info(movie)
        if not info:
            continue

        frame = tk.Frame(poster_frame, bg="#f0f0f0")
        frame.pack(side=tk.LEFT, padx=10)

        if info["poster_url"]:
            try:
                img_data = requests.get(info["poster_url"]).content
                img = Image.open(BytesIO(img_data))
                img = img.resize((140, 210))
                poster_img = ImageTk.PhotoImage(img)

                lbl = tk.Label(frame, image=poster_img, cursor="hand2", bg="#f0f0f0")
                lbl.image = poster_img
                lbl.pack()

                # Tooltip (hover info)
                tooltip_text = f"{info['genres']} | Rating: {info['rating']}\n\n{info['overview']}"
                CreateToolTip(lbl, tooltip_text)

                # Click → open YouTube trailer
                lbl.bind("<Button-1>", partial(lambda link, e: webbrowser.open_new_tab(link), info['youtube_search']))

                # Title + Rating + Genre
                title_lbl = tk.Label(frame, text=movie, font=("Arial", 10, "bold"), wraplength=140, bg="#f0f0f0")
                title_lbl.pack()
                meta_lbl = tk.Label(frame, text=f"{info['genres']}\n⭐ {info['rating']}", font=("Arial", 9), wraplength=140, bg="#f0f0f0", fg="#555")
                meta_lbl.pack()

            except Exception as e:
                print("Poster error:", e)

    poster_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))



# GUI SETUP
root = tk.Tk()
root.title("Smart Movie Recommender")
root.geometry("1000x700")
root.config(bg="#f0f0f0")

label = tk.Label(root, text="Enter Movie Title:", font=("Arial", 12), bg="#f0f0f0")
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12), width=40)
entry.pack()

btn = tk.Button(root, text="Get Recommendations", command=recommend,
                bg="#007acc", fg="white", font=("Arial", 12))
btn.pack(pady=10)

output = tk.Listbox(root, width=50, height=6, font=("Arial", 11))
output.pack(pady=10)

# SCROLLABLE POSTER AREA
canvas_frame = tk.Frame(root, bg="#f0f0f0")
canvas_frame.pack(pady=10, fill=tk.BOTH, expand=False)

canvas = tk.Canvas(canvas_frame, height=320, bg="#f0f0f0")
scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

poster_frame = tk.Frame(canvas, bg="#f0f0f0")
canvas.create_window((0, 0), window=poster_frame, anchor="nw")

root.mainloop()
