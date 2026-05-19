from flask import Flask, render_template
from dotenv import load_dotenv
import requests
import os
import datetime

app = Flask(__name__)

'''Variáveis de ambiente'''

load_dotenv()
api_key = os.getenv('API_KEY')
application_id = os.getenv('APPLICATION_ID')
application_secret = os.getenv('APPLICATION_SECRET')    


'''-----Home Page-----'''


'''Integração AstronomyAPI (Fase da lua)'''
url_moon_phase = "https://api.astronomyapi.com/api/v2/studio/moon-phase"
moon_params = {
    "format": "svg",
    "style": {
        "moonStyle": "default",
        "backgroundStyle": "solid",
        "backgroundColor": "black",
        "headingColor": "white",
        "textColor": "white"
    },
    "observer": {
        "latitude": 6.56774,
        "longitude": 79.88956,
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


'''Endpoint para a Home Page'''
@app.route("/index")
def index():
    return render_template("index.html", svg_moon = formated_data_moon)


'''-----APOD API-----'''


'''Integração APOD API NASA'''
data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
formatedData = data.json()
url_apod = formatedData['url']
txt_apod = formatedData['explanation']
media_type_apod = formatedData['media_type']


'''Endpoint para a imagem da APOD API'''
@app.route("/apod")
def apod():
    return render_template("apod.html", url = url_apod, description = txt_apod, media_type = media_type_apod)


'''-----Asteroids NeoWs API-----'''


'''Integração com a Asteroids NeoWS API NASA'''
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
for j in object_data:
    list_approach_date_full.append(j['close_approach_data'][0]['close_approach_date_full'])
all_data = list(zip(list_names, list_diameter, list_approach_date_full))


'''Endpoint para os dados da tabela de asteroides'''
@app.route("/asteroids")
def asteroids():
    return render_template("asteroids.html", count = object_count, data = all_data)