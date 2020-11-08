#!/usr/bin/env python
import json
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from datetime import datetime
from weather import weather_query, weather_rating
from maps import get_location, get_popular_times, get_places_autocomplete, Place, popular_times_ratings, location_stars_rating, current_popularity_rating, location_open_currently

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route("/submit" , methods=['POST'])
def result():
    # for the location that user specifies & alternatives, figure out weighting
    # Get the location information
    loc_data = json.loads(request.form["json_data"])
    lat = loc_data["latitude"]
    lng = loc_data["longitude"]
    zip_code = loc_data["zip_code"]
    place_id = loc_data["place_id"]

    # Get the raw data from API requests about the location
    weather_data = weather_query(lat, lng)
    popular_times_data = get_popular_times(place_id)

    # popular_times_scores & weather_scores hold 48 data points of ratings
    # for weather_scores, each has rating from 0 to 100
    # for popular_times_scores, each has rating from 0 onwards (max unknown)
    # stars_ratings_scores is a tuple (1st is number from 0.0 to 5.0, 2nd is # of ratings); basically if there are a lot of ratings we can trust the reviews
    # current_popularity_score is a single number from 0 onwards (max unknown); should be compared to values in popular_times_scores
    weather_scores = weather_rating(weather_data)
    popular_times_scores = popular_times_ratings(weather_data, popular_times_data)
    #stars_rating_scores = location_stars_rating(popular_times_data)
    current_popularity_score = current_popularity_rating(popular_times_data)
    open_string = location_open_currently(weather_data, popular_times_data)
    # do the weighting (bad = higher score)    
    print(open_string)
    if (popular_times_scores == []):
        # Popular times unavailable
        return json.dumps({"resp": "Data unavailable", "open": open_string })

    # Main Algorithm to find the best time in the next 48 hours to go
    aggregate_scores = []
    for i in range(48):
        aggregate_score = 0.0
        if (weather_scores != [] and popular_times_scores != [] and current_popularity_score != None):
            # Full information available
            aggregate_score += 0.1*(weather_scores[i]/100)
            aggregate_score += 0.6*(popular_times_scores[i]/max([val for val in popular_times_scores if val != 1000]))
            if (current_popularity_score > popular_times_scores[i]):
                # Case where the live popularity score is worse than the hour comparing to
                aggregate_score += 0.3
        elif (weather_scores == [] and popular_times_scores != [] and current_popularity_score != None):
            # Weather info unavailable
            aggregate_score += 0.65*(popular_times_scores[i]/max([val for val in popular_times_scores if val != 1000]))
            if (current_popularity_score > popular_times_scores[i]):
                # Case where the live popularity score is worse than the hour comparing to
                aggregate_score += 0.35
        elif (weather_scores != [] and popular_times_scores != [] and current_popularity_score == None):
            # Current popularity score unavailable
            aggregate_score += 0.15*(weather_scores[i]/100)
            aggregate_score += 0.85*(popular_times_scores[i]/max([val for val in popular_times_scores if val != 1000]))
        elif (weather_scores == [] and popular_times_scores != [] and current_popularity_score == None):
            # Weather info & current popularity unavailable
            aggregate_score += (popular_times_scores[i]/max([val for val in popular_times_scores if val != 1000]))
        aggregate_scores.append(aggregate_score)            
    
    # Based on the current time (from the weather API), get closest whole hour
    current_time = int(weather_data['current']['dt'])
    offset = current_time % 3600
    rounded_time = current_time - offset
    if (offset > 3600/2):
        time_closest_hour = rounded_time + 3600
    else:
        time_closest_hour = rounded_time

    best_hour_offset = 0
    best_hour_score = aggregate_scores[0]
    for i in range(len(aggregate_scores)):
        if (aggregate_scores[i] < best_hour_score):
            best_hour_offset = i
            best_hour_score = aggregate_scores[i]

    best_time = time_closest_hour + (best_hour_offset*60*60) # Unix timestamp

    # With the unix timestamp get the day of week and hour of the day
    best_time_string = datetime.fromtimestamp(best_time).strftime('%A, %B %d at %I %p').lstrip("0").replace(" 0", " ")

    return json.dumps({"resp": best_time_string, "open":open_string})

if __name__=='__main__':    
    app.run(debug=True)
