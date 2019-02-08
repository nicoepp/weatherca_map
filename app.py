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
    """
    Enpoint to get the current weather condition data of all cities at once

    Observations (if used in production):
    - The output of current_condition() should be cached for some time to not depend
      on the permformance and availablity of Environment Canada servers.
    - There could be an endpoint where the just the data of one city could be requested.
      With that the frontend would be able to parallelize the obtention of the data.
      For now I replaced a simple for loop with multiprocessing.Pool.map(callback, iterable)
      which gets an improvement of some seconds. See comment print statement at utils.py
    """
    try:
        city_weather_list = pool.map(current_condition, CITY_LIST)
    except IOError as e:
        return jsonify(data=[], message=str(e)), 500

    return jsonify(data=city_weather_list)


if __name__ == '__main__':
    app.run()
