from datetime import datetime
from cityweather import City, CityIndex

index = CityIndex()


def current_condition(cityname):
    """
    Helper function to get and format the data per city

    Observations (if used in production):
    - Maybe inherit and extend City from the cityweather library
      to make the code more object oriented.
    - This function could be unit tested with a mockup XML data source
    - Do more error checks and check also for empty data
    - Do better messages in case of errors and other unexpected behaviour
    - Extract (and display) more of the current condition data.
      The current data points are just a start to show doability.
    - The cityweather (mini)library should work with streams instead of
      passing the hole XML string into memory and then parsing it.

    :param cityname: The name of the city spelled exactly like in cityweather.CityIndex.english_city_list()
    :return: Dictionary structured in a clean format ready and easy to consume by a frontend
    """
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
        'time': dt.time().isoformat()[:-3] if dt else '',
        'temperature': float(city.get_quantity(temperature_str)),
        'condition': city.get_quantity(condition_str)
    }


def lat_to_float(lat_str):
    # Examples: "58.42N" to 58.42
    #           "48.52S" to -48.52
    sense = 1 if lat_str[-1:] == 'N' else -1
    num = float(lat_str[:-1])
    return num * sense


def long_to_float(lat_str):
    # Examples: "130.03W" to -130.03
    #           "123.03E" to 123.03
    sense = -1 if lat_str[-1:] == 'W' else 1
    num = float(lat_str[:-1])
    return num * sense

