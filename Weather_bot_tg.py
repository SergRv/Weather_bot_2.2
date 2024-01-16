import requests
import asyncio
from config import BOT_TOKEN, OPEN_WEATHER_TOKEN
from pprint import pprint
import datetime
import math
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Message
from translate import Translator


def degrees_to_cardinal(degree):
    dirs = ["Северный", "Северо-восточный", "Восточный", "Юго-восточный",
            "Южный", "Юго-западный", "Западный", "Северо-западный"]
    ix = int((degree + 11.25)/22.5)
    return dirs[ix % 8]


async def add_weather(message, weather_token=OPEN_WEATHER_TOKEN):
    try:
        translator = Translator(from_lang="russian", to_lang="english")
        translation = translator.translate(message.text)
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={translation}&appid={weather_token}&units=metric")
        data = request.json()
        city = data['name']
        temperature = math.floor(data['main']['temp'])
        pressure = math.floor(data['main']['pressure'] / 1.333)
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        deg_wind = degrees_to_cardinal(data['wind']['deg'])
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        day_light = sunset - sunrise

        await message.reply (f"Текущее время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: { city} \nТемпература: {temperature} C°\n"
              f"Влажность воздуха: {humidity} % \nДавление: {pressure} мм.рт.ст.\n"
              f"Скорость ветра: {wind} м/с \nНаправление ветра: {deg_wind} \nВосход солнца: {sunrise}\n"
              f"Закат солнца: {sunset} \nПродолжительность светового дня: {day_light}"
              )

    except Exception as ex:
        await message.reply('Такой город не найден!')


async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(let_start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



async def let_start(message: Message, bot: Bot):
    await message.answer("Привет, введи название города!")
    await add_weather(message,weather_token=OPEN_WEATHER_TOKEN)



if __name__ == '__main__':
    asyncio.run(start_bot())