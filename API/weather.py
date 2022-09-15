import requests
import json

WEATHER_TOKEN = "1239f2f8c244ddf9454c22a3e8fb1ca3"
LOCATE = "Lutsk"

def get_weather(city, weather_token):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric")
    data = r.json()
    temp = int(data["main"]["temp"])
    cur_weather =""
    degrees = "градусів"
    if temp < 5:
        degrees = "градуса" 
    if temp < 0:
        cur_weather = f"мінусова температура {temp} {degrees}"
    else:
        cur_weather = f"пльусова тeмпература {temp} {degrees}"

    return cur_weather

