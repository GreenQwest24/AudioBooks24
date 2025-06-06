# Import necessary libraries
from flask import Flask, render_template, request, send_file
import pyttsx3
import os
import json

# Create a Flask application instance
app = Flask(__name__)

# Define the path to the ebooks and audiobooks directories
EBOOKS_PATH = "static/ebooks"
AUDIOBOOKS_PATH = "static/audiobooks"

# Load all eBooks from a JSON file (contains titles and content)
with open("ebooks.json", "r") as f:
    ebooks = json.load(f)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech and save as mp3
def convert_to_audio(title, content):
    audio_file = os.path.join(AUDIOBOOKS_PATH, f"{title}.mp3")
    if not os.path.exists(audio_file):
        engine.save_to_file(content, audio_file)
        engine.runAndWait()
    return audio_file

# Route for the homepage
@app.route("/")
def index():
    # Render the index.html template with the list of ebooks
    return render_template("index.html", ebooks=ebooks)

# Route to read the book
@app.route("/read")
def read():
    # Get the title of the requested book from the URL
    title = request.args.get("title")
    # Find the ebook data by title
    book = next((book for book in ebooks if book["title"] == title), None)
    # Render the read.html page and pass the book content
    return render_template("read.html", book=book)

# Route to download the ebook text file
@app.route("/download")
def download():
    title = request.args.get("title")
    filename = f"{title}.txt"
    filepath = os.path.join(EBOOKS_PATH, filename)
    return send_file(filepath, as_attachment=True)

# Route to listen to audiobook
@app.route("/listen")
def listen():
    title = request.args.get("title")
    # Get book content
    book = next((book for book in ebooks if book["title"] == title), None)
    # Convert the content to audio (if not already converted)
    audio_file = convert_to_audio(title, book["content"])
    # Render a page with an HTML5 audio player
    return render_template("listen.html", title=title, audio_path=f"/{audio_file}")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
2
