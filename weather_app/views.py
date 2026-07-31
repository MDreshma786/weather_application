
from .models import Weather
import requests
import environ
from django.shortcuts import render
env = environ.Env()

def home(request):
    weather = None
    error = None

    # Last searched city
    last_city = request.session.get("last_city")

    if request.method == "POST":

        city = request.POST.get("city", "").strip()

        if city:

            # Save last searched city in session
            request.session["last_city"] = city
            last_city = city

            api_key = env("API_KEY")

            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"

            response = requests.get(url)

            data = response.json()

            if response.status_code == 200:

                weather = {
                    "city": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "temp": data["current"]["temp_c"],
                    "humidity": data["current"]["humidity"],
                    "wind": data["current"]["wind_kph"],
                    "condition": data["current"]["condition"]["text"],
                    "icon": "https:" + data["current"]["condition"]["icon"],
                }

            else:
                error = data.get("error", {}).get("message", "City not found.")

    return render(request, "home.html", {
        "weather": weather,
        "last_city": last_city,
        "error": error,
    })