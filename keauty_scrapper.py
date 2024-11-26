import requests
from bs4 import BeautifulSoup

url = 'https://keauty.ru/catalog/brand/SECRET-SKIN/?in-stock=on'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    prices = soup.find_all('span', class_='total-price')
    for price in prices:
        print(price.text)
else:
    print(f'Ошибка: {response.status_code}')