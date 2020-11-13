from datetime import datetime
import os
import pytz
import requests
import math
import livepopulartimes
# Google Maps API Key
API_KEY = 'GOOGLE_MAPS_API_KEY'
# Popular Times API Key 
API_KEY_PT = 'GOOGLE_POPULAR_TIMES_API_KEY'

# Google Places Autocomplete API Key and URL
API_KEY_AUTO = 'GOOGLE_PLACES_AUTOCOMPLETE_API_KEY' 
API_URL_AUTO = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?origin={0},{1}&location={0},{1}&key={2}&input=pizza'

# Google Places Details API Key and URL
API_KEY_DET = 'GOOGLE_PLACES_DETAILS_API_KEY'
API_URL_DET = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=geometry,opening_hours&key={}'



def get_location(ip_address):
    data = (None, None, None)
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        data = (js['lat'], js['lon'], js['zip'])
    except Exception as e:
        print(e)
    return data

# GOOGLE PLACES AUTOCOMPLETE API
def get_places_autocomplete(latitude, longitude):
	try:
		response = requests.get(API_URL_AUTO.format(latitude, longitude, API_KEY_AUTO)).json()
		if response["status"] != "OK":
			print("PLACES AUTOCOMPLETE ERROR: {}".format(response["error_message"]))
			data_json = None
	except Exception as e:
		print(e)
		data_json = None
	return data_json



def get_popular_times(place_id):
	data = None
	try:
		data = livepopulartimes.get_populartimes_by_PlaceID(API_KEY_PT, place_id)
	except Exception as e:
		print(e)
	return data

def popular_times_ratings(weather_data, popular_times_data):
    # Function used to get 48 data points corresponding to next 48 hrs of the popular times
    popular_times_scores = []
    # Case where the data is unavailable
    if ('populartimes' not in popular_times_data):
        return popular_times_scores
    # Based on the current time (from the weather API), get closest whole hour
    current_time = int(weather_data['current']['dt'])
    offset = current_time % 3600
    rounded_time = current_time - offset
    if (offset > 3600/2):
        time_closest_hour = rounded_time + 3600
    else:
        time_closest_hour = rounded_time

    # With the unix timestamp get the day of week and hour of the day
    hour = int(datetime.fromtimestamp(time_closest_hour).strftime('%H')) #0 - 23
    day_of_week = int(datetime.fromtimestamp(time_closest_hour).strftime('%w')) #0 = Sunday

    # Then get 48 hours of populartimes data from that point
    current_hour = hour
    # Days of week in populartimes API are 0 = Monday and so on 
    current_day_of_week = day_of_week - 1
    if (current_day_of_week < 0): #edge case for Sunday mapping 0 -> 6
        current_day_of_week = 6
    current_time_closest_hour = time_closest_hour

    while(current_time_closest_hour < time_closest_hour + 48*60*60):
        # From the popular_times_data, find the corresponding popularity of the current_hour & add to popular_times_scores
        # If location is open, just append normal time, else append a very large number so that time cannot be used (since closed)
        try:
            open_time = int(popular_times_data['hours']['periods'][current_day_of_week]['open']['time'])
            close_time = int(popular_times_data['hours']['periods'][current_day_of_week]['close']['time'])
            if (open_time < (current_hour * 100) < close_time):
                popular_times_scores.append(popular_times_data['populartimes'][current_day_of_week]['data'][current_hour])
            else:
                popular_times_scores.append(1000)
        except Exception as e:
            # Case that open/close time unavailable
            if (popular_times_data['populartimes'][current_day_of_week]['data'][current_hour] != 0):
                popular_times_scores.append(popular_times_data['populartimes'][current_day_of_week]['data'][current_hour])
            else:
                popular_times_scores.append(1000)

        if (current_hour == 23):
            current_day_of_week += 1
            if (current_day_of_week > 6): #Going from Sun (6) -> Mon (0)
                current_day_of_week = 0
        current_hour = (current_hour + 1) % 24
        current_time_closest_hour += 3600

    return popular_times_scores

def location_stars_rating(popular_times_data):
    if ('rating' in popular_times_data):
        return (popular_times_data['rating'], popular_times_data['rating_n'])
    # If field is unavailable, return None
    return (None, None)

def current_popularity_rating(popular_times_data):
    if ('current_popularity' in popular_times_data):
        return popular_times_data['current_popularity']
    # If field is unavailable, return None
    return None

def location_open_currently(weather_data, popular_times_data):
    if ('current' not in weather_data):
        return "Unknown"
    current_time = int(weather_data['current']['dt'])
    # With the unix timestamp get the day of week and hour of the day
    hour = int(datetime.fromtimestamp(current_time).strftime('%H')) #0 - 23
    day_of_week = int(datetime.fromtimestamp(current_time).strftime('%w')) #0 = Sunday

    # Then get 48 hours of populartimes data from that point
    current_hour = hour
    # Days of week in populartimes API are 0 = Monday and so on 
    current_day_of_week = day_of_week - 1
    if (current_day_of_week < 0): #edge case for Sunday mapping 0 -> 6
        current_day_of_week = 6
    try:
        open_time = int(popular_times_data['hours']['periods'][current_day_of_week]['open']['time'])
        close_time = int(popular_times_data['hours']['periods'][current_day_of_week]['close']['time'])
        if (open_time < (current_hour * 100) < close_time):
            return "Currently open"
        else:
            return "Currently closed"           
    except Exception as e:
        # No open/close time
        return "Unknown"
