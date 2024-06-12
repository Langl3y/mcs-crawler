import random
import time
import re

from lxml import html
from utils import *


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


def yamaha_bike_crawler(bike_url):
    html_string = get_html(bike_url)
    document = html.fromstring(html_string)
    try:
        bike_name_element = document.xpath('/html[1]/body[1]/main[1]/div[1]/div[1]/div[1]/h1[1]/text()')
        bike_price_element = document.xpath('/html[1]/body[1]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]/p[1]')
    except:
        bike_name_element = document.xpath('/html[1]/body[1]/header[1]/div[1]/ul[1]/li[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/strong[1]/text()')
        bike_price_element = document.xpath('/html[1]/body[1]/header[1]/div[1]/ul[1]/li[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/p[1]/span[1]')

    bname = ''
    bprice = 0

    if bike_name_element:
        bname = bike_name_element[0].strip()

    for price_element in bike_price_element:
        price_string = price_element.text_content().strip()
        cleaned_price = re.sub(r'[^\d]+', '', price_string)
        bprice = int(cleaned_price)

    return bname, bprice


def extract_links(xpath_pattern, start_index=1):
    html_string = get_html(yamaha_base_url)
    document = html.fromstring(html_string)

    index = start_index
    links = []

    while True:
        try:
            xpath = xpath_pattern.format(index)
            elements = document.xpath(xpath)
            if not elements:
                break
            for element in elements:
                href = element.get('href')
                text = element.text_content().strip() if element.text_content() else 'No text'
                links.append((href, text))
            index += 1
        except IndexError:
            break

    return links


def yamaha_crawler():
    yamaha_bikes_data = []
    yamaha_links = []

    xpath_patterns = [
        '/html[1]/body[1]/main[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[{}]/div[1]/a[1]',
        '/html[1]/body[1]/main[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[{}]/div[1]/a[1]',
        '/html[1]/body[1]/main[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div[{}]/div[1]/a[1]'
    ]

    for xpath_pattern in xpath_patterns:
        links = extract_links(xpath_pattern)
        yamaha_links.extend(links)

    for yamaha_link in yamaha_links:
        clean_url = yamaha_link[0].strip("('")
        clean_url = clean_url.rstrip("',)")
        bike_url = f'{clean_url}'
        print(bike_url)
        bname, bprice = yamaha_bike_crawler(bike_url)
        yamaha_bikes_data.append((bname, bprice))

    print(yamaha_bikes_data)
    return yamaha_bikes_data


yamaha_base_url = 'https://yamaha-motor.com.vn/xe/'
bikes_data = yamaha_crawler()
write_to_csv(bikes_data)
