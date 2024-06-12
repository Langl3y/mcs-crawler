import random
import time
import re

from lxml import html
from utils import *

logger = logging.getLogger('crawl')


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


def ktm_bike_crawler(bike_url):
    html_string = get_html(bike_url)
    document = html.fromstring(html_string)

    bike_name_element = document.xpath('/html[1]/body[1]/div[3]/div[1]/section[1]/div[1]/div[1]/h1[1]')
    bike_price_element = document.xpath('/html[1]/body[1]/div[3]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/span[1]')

    bname = ''
    bprice = 0

    for name_element in bike_name_element:
        bname = name_element.text_content().strip()

    for price_element in bike_price_element:
        price_text = price_element.text_content().strip()

        price_without_dots = price_text.replace('.', '')

        numeric_price = re.search(r'\d+', price_without_dots)
        if numeric_price:
            bprice = int(numeric_price.group())

    return bname, bprice


def extract_links(xpath_pattern, start_index=1):
    html_string = get_html(ktm_base_url)
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


def ktm_crawler():
    ktm_bikes_data = []
    xpath_pattern = '/html[1]/body[1]/div[3]/div[1]/section[1]/div[1]/div[1]/div[1]/div[{}]/a[1]'
    ktm_links = extract_links(xpath_pattern)

    for ktm_link in ktm_links:
        clean_url = ktm_link[0].strip("('")
        clean_url = clean_url.rstrip("',)")
        bike_url = f'{clean_url}'
        print(bike_url)
        bname, bprice = ktm_bike_crawler(bike_url)
        ktm_bikes_data.append((bname, bprice))

    print(ktm_bikes_data)
    return ktm_bikes_data


ktm_base_url = 'https://ktmvietnam.vn/mo-to/'
bikes_data = ktm_crawler()
write_to_csv(bikes_data)
