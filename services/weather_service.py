
import requests


def clean_rainfall_value(value):
    try:
        value = float(value)

        if value < 0:
            return 0.0

        return value

    except (TypeError, ValueError):
        return 0.0


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation",
        "past_hours": 72,
        "forecast_hours": 1,
        "timezone": "Asia/Kolkata"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        rainfall = data["hourly"]["precipitation"]
        times = data["hourly"]["time"]

        clean_rainfall = []

        for value in rainfall:
            value = clean_rainfall_value(value)
            clean_rainfall.append(value)

        rainfall_1h = clean_rainfall[-1]
        rainfall_6h = sum(clean_rainfall[-6:])
        rainfall_24h = sum(clean_rainfall[-24:])
        rainfall_72h = sum(clean_rainfall[-72:])

        latest_timestamp = times[-1]

        weather_data = {
            "latitude": round(latitude, 4),
            "longitude": round(longitude, 4),
            "rainfall_1h": round(rainfall_1h, 2),
            "rainfall_6h": round(rainfall_6h, 2),
            "rainfall_24h": round(rainfall_24h, 2),
            "rainfall_72h": round(rainfall_72h, 2),
            "timestamp": latest_timestamp
        }

        return weather_data

    except requests.exceptions.RequestException as error:
        print("Weather API failed.")
        print("Error:", error)
        return None

    except (KeyError, TypeError, ValueError) as error:
        print("Invalid weather data received.")
        print("Error:", error)
        return None
