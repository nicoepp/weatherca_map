from flask import Flask, jsonify, render_template
from utils import current_condition

app = Flask(__name__)

CITY_LIST = [
    'Dease Lake',
    'Fort Nelson',
    'Terrace',
    'Prince George',
    'Whistler',
    'Revelstoke',
    'Creston'
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/conditions/all')
def conditions():
    city_weather_list = []

    for city_name in CITY_LIST:
        result = current_condition(city_name)
        city_weather_list.append(result)

    return jsonify(data=city_weather_list)


if __name__ == '__main__':
    app.run()
