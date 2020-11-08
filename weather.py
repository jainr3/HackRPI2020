from datetime import datetime
import os
import pytz
import requests
import math
import json
API_KEY = 'OPEN_WEATHER_MAP_API_KEY' 
API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,alerts&appid={}')


def weather_query(lat, lon):    
    try:        
        print(API_URL.format(lat, lon, API_KEY))        
        data = requests.get(API_URL.format(lat, lon, API_KEY)).json()    
    except Exception as exc:        
        print(exc)        
        data = None    
    return data


def weather_rating(data):
    # Takes in raw data from weather query
    # Returns list (size 48) for hourly weather ratings
    # Data points for 48 hours from current time
    f = open('static/weather_codes.json')

    output_ratings = []
    weather_ratings = json.load(f)

    if(data['hourly'] == None):
        return output_ratings

    for hour in data['hourly']:
        #current_hour = datetime.fromtimestamp(int(hour['dt'])).strftime('%H')
        rating = weather_ratings['weather'][str(hour['weather'][0]['id'])]
        output_ratings.append(int(rating))

    return output_ratings
