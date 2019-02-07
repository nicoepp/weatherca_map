from datetime import datetime
from cityweather import City, CityIndex

index = CityIndex()


def current_condition(cityname):
    station_str = 'currentConditions/station'
    condition_str = 'currentConditions/condition'
    temperature_str = 'currentConditions/temperature'
    date_text_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/textSummary"
    timestamp_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/timeStamp"

    city = City(index.data_url(cityname))
    time_stamp = city.get_quantity(timestamp_str)
    text_summary = city.get_quantity(date_text_str)
    dt = datetime.strptime(time_stamp, '%Y%m%d%H%M%S') if time_stamp else None

    return {
        'station': city.get_quantity(station_str),
        'location': {
            'lat': city.get_attribute(station_str, "lat"),
            'lng': city.get_attribute(station_str, "lon")
        },
        'date_time_text': text_summary if text_summary else '',
        'date': dt.date().isoformat() if dt else '',
        'time': dt.time().isoformat() if dt else '',
        'temperature': city.get_quantity(temperature_str),
        'condition': city.get_quantity(condition_str)
    }
