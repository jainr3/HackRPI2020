# HackRPI2020

## Inspiration

In the age of Covid-19, people are uncertain about the best times to go to certain places like grocery shopping. Our project aims to make it easier for people to get suggestions about the best time to travel.

## What it does

The user types in the desired location into a search bar and the application autocompletes the query. Once the location has been entered, the map zooms into the desired location and provides the address, if it is currently open, and when the best time to go to the location is (within a range of 2 days or 48 hours from the current time).

## How I built it

The technologies we used include Flask, Python, JavaScript, HTML, and Ajax. To retrieve the relevant data points for popular times of a location we utilized the [popular-times-api](https://pypi.org/project/LivePopularTimes/), [google-places-api](https://developers.google.com/places/web-service/overview), [google-maps-javascript-api](https://developers.google.com/maps/documentation/javascript/overview). The algorithm that we developed takes in hourly data for the next 48 hours of popular-times and weather-data. It also takes into account the live-popular-times data that is available for certain locations. For example, some locations have a live view of how many people are at the location and this number can be compared to the expected values for the 48 data points.

## Challenges I ran into

Figuring out the layout of the application was difficult since we wanted to balance functionality with aesthetics. We also had trouble working out pieces of JavaScript code since it was the first time that we had worked with it. There are still a few bugs with the application that we were not able to resolve, but fortunately they are of low severity. 

## Accomplishments that I'm proud of

We are proud that we were able to develop a proof of concept for the project and we are also glad that we were able to learn how to use new tools like Flask & Google APIs.

## What I learned

We learned a lot about technical skills with the new technologies and we also learned how to work remotely with each other using VS Code Share.

## What's next for Travel Times

We would firstly like to improve the algorithm and optimize the weights to be more objective. The algorithm could also potentially take in more data such as live / expected traffic data and potentially Yelp reviews. In addition, the user workflow is one-sided right now as it supports only specific locations that are filled in with autocomplete. To improve this, we could support queries like "Pizza places near me" and then compare and rank locations based on distance, ratings, and the popular-times / weather data (that was already being used). As always, we could refactor the code to be more readable and have thorough error checking.

## Miscellaneous
[Tutorial to get started](https://www.freecodecamp.org/news/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221/)
[Google Cloud Platform](https://console.cloud.google.com/)
Commands to run to get started with Python's virtual environment:
* pip install virtualenvwrapper-winpip install virtualenv
* mkdir WeatherAppcd WeatherAppvirtualenv venv
* call venv\Scripts\activate.bat
* pip install -r requirements.txt
* **python main.py**
* Open http://127.0.0.1:5000/

Commands to deploy to Google Cloud
* Install the Google Cloud SDK
* Create the app
* gcloud app deploy
