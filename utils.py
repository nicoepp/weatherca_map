from datetime import datetime
from cityweather import City


def current_condition(index, cityname):
    station_str = 'currentConditions/station'
    condition_str = 'currentConditions/condition'
    temperature_str = 'currentConditions/temperature'
    date_text_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/textSummary"
    timestamp_str = "currentConditions/dateTime[@name='observation'][@zone='PST'][@UTCOffset='-8']/timeStamp"

    city = City(index.data_url(cityname))
    ts = city.get_quantity(timestamp_str)
    if ts:
        dt = datetime.strptime(ts, '%Y%m%d%H%M%S')
    else:
        dt = None

    print(f'Station: {city.get_quantity(station_str)}')
    print(f'Date: {dt.date().isoformat() if dt else "?"}')
    print(f'Time: {dt.time().isoformat() if dt else "?"}')
    print()
    print(f'Temp: {city.get_quantity(temperature_str)}')
    print(f'Condition: {city.get_quantity(condition_str)}')
    print('=====')
