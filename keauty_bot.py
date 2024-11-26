import time
import schedule
import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = '7406516259:AAFixDTBfRlp5Gba3voNWwkcjZ0C28nexMo'
CHAT_ID = '1853362849'

bot = telebot.TeleBot(TOKEN)
#bot.send_message(CHAT_ID, "Привет! Это тестовое сообщение.")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для отслеживания цен. Я уведомлю тебя, если цена упадет!")

bot.polling()

def get_price():
    url = 'https://keauty.ru/catalog/brand/SECRET-SKIN/?in-stock=on'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        prices = soup.find_all('span', class_='total-price')
        for price in prices:
            print(price.text)
    else:
        print(f'Ошибка: {response.status_code}')
    return 1000

last_price = get_price()

while True:
    current_price = get_price()
    if current_price < last_price:
        message = f'Цена на товар упала! Сейчас она {current_price} руб.'
        bot.send_message(CHAT_ID, message)
        last_price = current_price
    time.sleep(3600)

def check_price():
    current_price = get_price()
    if current_price < last_price:
        message = f'Цена на товар упала! Сейчас она {current_price} руб.'
        bot.send_message(CHAT_ID, message)
        last_price = current_price

schedule.every(1).hour.do(check_price())

while True:
    schedule.run_pending()
    time.sleep(1)