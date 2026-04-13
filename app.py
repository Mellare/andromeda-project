from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/apod")
def apod():
    data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    formatedData = data.json()
    url_img = formatedData['url']
    return render_template("apod.html", img_apod = url_img)