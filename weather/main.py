from datetime import datetime

import requests

from config import parameters, url
from db import query as sql
# from db.query import *


def get_weather():
    username = input('username: ')
    is_exists, user_id = sql.check_user_exists("weather.db", username)  # (False, False)
    if not is_exists:
        sql.add_user("weather.db", username)
        get_weather()
    else:
        while True:
            city = input("Введите город, в котором хотите узнать погоду: ")

            if city == "save":
                print("save")
                continue
            elif city == "history":
                data = sql.get_user_history("weather.db", user_id)
                if not data:
                    print('empty history')

                for item in data:
                    print(item[1:-1])
                continue
            elif city == "clear":
                sql.clear_history("weather.db", user_id)
                print('cleared')
                continue

            parameters["q"] = city

            resp = requests.get(url, params=parameters).json()
            tz = resp["timezone"]
            dt = datetime.utcfromtimestamp(resp["dt"] + tz).strftime("%Y:%m:%d %H:%M:%S")
            temp = resp["main"]["temp"]
            name = resp["name"]
            sunrise = datetime.utcfromtimestamp(resp["sys"]["sunrise"] + tz).strftime("%Y:%m:%d %H:%M:%S")
            sunset = datetime.utcfromtimestamp(resp["sys"]["sunset"] + tz).strftime("%Y:%m:%d %H:%M:%S")
            description = resp["weather"][0]["description"]
            speed = resp["wind"]["speed"]

            sql.add_weather("weather.db",
                            name=name,
                            tz=tz,
                            dt=dt,
                            sunrise=sunrise,
                            sunset=sunset,
                            temp=temp,
                            description=description,
                            speed=speed,
                            user_id=user_id)

            print(f"""
=========================
В городе {name} сейчас {description}
Температура: {temp}
Скорость ветра: {speed}
Восход солнца: {sunrise}
Закат солнца: {sunset}
Время отправки запроса: {dt}
""")
