from flask import Flask, jsonify, render_template
from utils import current_condition
import multiprocessing


pool = multiprocessing.Pool()

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
    city_weather_list = pool.map(current_condition, CITY_LIST)

    return jsonify(data=city_weather_list)


if __name__ == '__main__':
    app.run()
