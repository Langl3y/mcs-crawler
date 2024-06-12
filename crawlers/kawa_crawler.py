import logging
import random
import time
import json
import re

from lxml import html
from utils import *

logger = logging.getLogger('crawl')

with open('../configs/config.json', 'r') as json_file:
    config = json.load(json_file)

with open('../urls.json', 'r') as url_file:
    urls = json.load(url_file)


def extract_price(price_text):
    price_text = re.sub(r'[^\d\.,]', '', price_text)
    price_text = price_text.strip(',.')

    if ' - ' in price_text:
        prices = price_text.split(' - ')
        first_price = float(prices[0].replace(',', ''))
        last_price = float(prices[1].replace(',', ''))
        return first_price, last_price
    else:
        cleaned_price = re.sub(r'[^0-9,]', '', price_text)
        price_value = float(cleaned_price.replace(',', ''))

        if '.' in str(price_value):
            price_value = int(price_value)

        return price_value


def kawa_bike_crawler(bike_url):
    html_string = get_html(bike_url)
    document = html.fromstring(html_string)

    bike_name = document.xpath(config['CONFIG_BIKE_NAME_KAWA_DETAIL'])
    bike_price = document.xpath(config['CONFIG_BIKE_PRICE_KAWA_DETAIL'])

    bname = ''
    bprice = 0

    for name in bike_name:
        bname = name.text.strip()

    for price in bike_price:
        price_text = price.text.strip()
        price_value = extract_price(price_text)
        if isinstance(price_value, tuple):
            first_price, last_price = price_value
            bprice = int(str(first_price)[:9]) - int(str(last_price)[:9])
        elif price_value == 0:
            bprice = 0
        elif price_value:
            bprice = int(str(price_value)[:9])
        else:
            bprice = 'Unknown'

    return bname, bprice


def extract_links(xpath_pattern, start_index=1):
    html_string = get_html('https://www.kawasaki-motors.vn')
    document = html.fromstring(html_string)

    index = start_index
    links = []

    while True:
        try:
            xpath = xpath_pattern.format(index)
            elements = document.xpath(xpath)
            if not elements:
                break  # If no more elements are found, break the loop
            for element in elements:
                href = element.get('href')
                text = element.text_content().strip() if element.text_content() else 'No text'
                links.append((href, text))
            index += 1
        except IndexError:
            break

    return links


def kawa_crawler():
    kawa_bikes_data = []
    xpath_pattern = '/html[1]/body[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[{}]/a[1]'
    kawa_links = extract_links(xpath_pattern)

    for kawa_link in kawa_links:
        clean_url = kawa_link[0].strip("('")
        clean_url = clean_url.rstrip("',)")
        bike_url = f'{kawa_base_url}{clean_url}'
        print(bike_url)
        bname, bprice = kawa_bike_crawler(bike_url)
        kawa_bikes_data.append((bname, bprice))

    print(kawa_bikes_data)
    return kawa_bikes_data


kawa_base_url = urls['KAWA_BASE_URL']
bikes_data = kawa_crawler()
write_to_csv(bikes_data)
