import requests
from config import BOT_TOKEN, OPEN_WEATHER_TOKEN
from pprint import pprint
import datetime
import math


def degrees_to_cardinal(degree):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((degree + 11.25)/22.5)
    return dirs[ix % 16]


def add_weather(city, OPEN_WEATHER_TOKEN):
    try:
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_TOKEN}&units=metric")
        data = request.json()
        city = data['name']
        temperature = math.floor(data['main']['temp'])
        pressure = math.floor(data['main']['pressure'] / 1.333)
        humidity = data['main']['humidity']
        wind = math.floor(data['wind']['speed'])
        deg_wind = degrees_to_cardinal(data['wind']['deg'])
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        day_light = sunset - sunrise

        print(f"Текущее время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: { city} \nТемпература: {temperature} C°\n"
              f"Влажность воздуха: {humidity} % \nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind} м/с \nНаправление ветра: {deg_wind} \nВосход солнца: {sunrise}\n"
              f"Закат солнца: {sunset} \nПродолжительность светового дня: {day_light}"
              )


    except Exception as ex:
        print(ex)
        print('Где-то ошибка!')


def main():
    city = input('Введите название города: ')
    add_weather(city, OPEN_WEATHER_TOKEN)


if __name__ == '__main__':
    main()
