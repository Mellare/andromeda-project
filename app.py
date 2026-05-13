from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os
import datetime

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')


'''Home Page'''
@app.route("/index")
def index():
    return render_template("index.html")

'''Apod API'''
data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
formatedData = data.json()
url_apod = formatedData['url']
txt_apod = formatedData['explanation']
media_type_apod = formatedData['media_type']

@app.route("/apod")
def apod():
    return render_template("apod.html", url = url_apod, description = txt_apod, media_type = media_type_apod)

'''Asteroids NeoWs API'''
data = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={datetime.date.today()}&end_date={datetime.date.today()}&api_key={api_key}")
formatedData = data.json()
object_count = formatedData['element_count']
object_data = formatedData['near_earth_objects'][f"{datetime.date.today()}"]
list_names = []
list_diameter = []
list_approach_date_full = []
for i in object_data:
    list_names.append(i['name'])
    list_diameter.append(i['estimated_diameter']['meters']['estimated_diameter_max'])
'''print(list_names)
print("------------------------------------------------------")
print(list_diameter)
print("------------------------------------------------------")'''
for j in object_data:
    list_approach_date_full.append(j['close_approach_data'][0]['close_approach_date_full'])
'''print(list_approach_date_full)
print("------------------------------------------------------")'''
all_data = list(zip(list_names, list_diameter, list_approach_date_full))

@app.route("/asteroids")
def asteroids():
    return render_template("asteroids.html", count = object_count, data = all_data)