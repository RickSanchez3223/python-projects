import requests
from bs4 import BeautifulSoup as Bs


def get_currency(from_c, to_c):
    url = f'https://www.x-rates.com/calculator/?from={from_c}&to={to_c}&amount=1'
    content = requests.get(url).text
    soup = Bs(content, 'html.parser')
    rate = soup.find('span', class_='ccOutputRslt').get_text()
    rate = rate[:-4]
    print(rate)

get_currency('EUR', 'AUD')
