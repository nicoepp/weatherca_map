from datetime import datetime
from cityweather import City, CityIndex

index = CityIndex()


def current_condition(cityname):
    station_str = 'currentConditions/station'
    condition_str = 'currentConditions/condition'
    temperature_str = 'currentConditions/temperature'
    date_text_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/textSummary"
    timestamp_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/timeStamp"

    # To measure the improvement of the concurrency just uncomment this line
    # print(f'At {datetime.now().time().isoformat()} doing {cityname}')

    city = City(index.data_url(cityname))
    loc_lat = city.get_attribute(station_str, "lat")
    loc_long = city.get_attribute(station_str, "lon")
    time_stamp = city.get_quantity(timestamp_str)
    text_summary = city.get_quantity(date_text_str)
    dt = datetime.strptime(time_stamp, '%Y%m%d%H%M%S') if time_stamp else None

    return {
        'name': cityname,
        'station': city.get_quantity(station_str),
        'location': {
            'lat': lat_to_float(loc_lat),
            'lng': long_to_float(loc_long)
        },
        'date_time_text': text_summary if text_summary else '',
        'date': dt.date().isoformat() if dt else '',
        'time': dt.time().isoformat() if dt else '',
        'temperature': float(city.get_quantity(temperature_str)),
        'condition': city.get_quantity(condition_str)
    }


def lat_to_float(lat_str):
    sense = 1 if lat_str[-1:] == 'N' else -1
    num = float(lat_str[:-1])
    return num * sense


def long_to_float(lat_str):
    sense = -1 if lat_str[-1:] == 'W' else 1
    num = float(lat_str[:-1])
    return num * sense

