from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os
import datetime

app = Flask(__name__)

'''-----Variáveis de ambiente-----'''

load_dotenv()
api_key = os.getenv('API_KEY')
application_id = os.getenv('APPLICATION_ID')
application_secret = os.getenv('APPLICATION_SECRET')    


@app.route("/index", methods=['GET', 'POST'])
def index():
    url_moon_phase = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
    moon_params = {
        "format": "svg",
        "style": {
            "moonStyle": "default",
            "backgroundStyle": "solid",
            "backgroundColor": "white",
            "headingColor": "black",
            "textColor": "black"
        },
        "observer": {
            "latitude": -23.5489,
            "longitude": -46.6388,
            "date": f"{datetime.date.today()}"
        },
        "view": {
            "type": "landscape-simple",
            "orientation": "north-up"
        }
    }
    data = requests.post(url_moon_phase, json = moon_params, auth = (application_id, application_secret))
    formated_data = data.json()
    formated_data_moon = formated_data['data']['imageUrl']
    return render_template("index.html", svg_moon = formated_data_moon)


@app.route("/apod", methods=['GET'])
def apod():
    data_apod = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    formated_data = data_apod.json()
    url_apod = formated_data['url']
    txt_apod = formated_data['explanation']
    media_type_apod = formated_data['media_type']
    return render_template("apod.html", url = url_apod, description = txt_apod, media_type = media_type_apod)


@app.route("/asteroids", methods=['GET'])
def asteroids():
    data_neoWs = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={datetime.date.today()}&end_date={datetime.date.today()}&api_key={api_key}")
    formated_data = data_neoWs.json()
    object_count = formated_data['element_count']
    object_data = formated_data['near_earth_objects'][f"{datetime.date.today()}"]
    list_names = []
    list_diameter = []
    list_approach_date_full = []
    for i in object_data:
        list_names.append(i['name'])
        list_diameter.append(i['estimated_diameter']['meters']['estimated_diameter_max'])
    for j in object_data:
        list_approach_date_full.append(j['close_approach_data'][0]['close_approach_date_full'])
    all_data = list(zip(list_names, list_diameter, list_approach_date_full))
    return render_template("asteroids.html", count = object_count, data = all_data)


@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(429)
def too_many_requests(error):
    return render_template("errors/429.html"), 429

@app.errorhandler(502)
def bad_gateway(error):
    return render_template("errors/502.html"), 502

@app.errorhandler(503)
def service_unavailable(error):
    return render_template("errors/503.html"), 503