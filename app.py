from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')
data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
formatedData = data.json()
print()
print(f"URL do dia: {formatedData['url']}\nInformações: {formatedData['explanation']}")

@app.route("/apod")
def apod():
    return render_template("apod.html")