import csv
import logging
import random
import time
import json
import re
import os
from datetime import datetime
import requests
from requests import session
from fake_useragent import UserAgent
from lxml import html

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


def triumph_bike_crawler(bike_url):
    html_string = get_html(bike_url)
    document = html.fromstring(html_string)

    bike_name = document.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/h1[1]')
    bike_price = document.xpath('/html[1]/body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/p[2]/span[2]')

    bname = ''
    bprice = 0

    for name in bike_name:
        bname = name.text.strip()

    for price in bike_price:
        price_text = price.text.strip()
        cleaned_price = re.sub(r'[^\d]+', '', price_text)
        bprice = int(cleaned_price)

    return bname, bprice


def extract_links(triumph_base_url, xpath_pattern, start_index=1):
    html_string = get_html(triumph_base_url)
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


def triumph_crawler(triumph_base_url):
    triumph_bikes_data = []
    xpath_pattern = '/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[{}]/a[1]'
    triumph_links = extract_links(triumph_base_url, xpath_pattern)

    for triumph_link in triumph_links:
        clean_url = triumph_link[0].strip("('")
        clean_url = clean_url.rstrip("',)")
        bike_url = f'{triumph_base_url}/{clean_url}'
        print(bike_url)
        bname, bprice = triumph_bike_crawler(bike_url)
        triumph_bikes_data.append((bname, bprice))

    print(triumph_bikes_data)
    return triumph_bikes_data


def write_to_csv(data, filename='../product_template.csv'):
    header = ["id", "name", "product_variant_ids/id", "cost_method", "list_price", "lst_price"]
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        for i, (name, price) in enumerate(data, start=2):
            writer.writerow([f"__export__.product_template_{i}", name, f"__export__.product_product_{i}", "Standard Price", price, price])


def get_html(url):
    headers = {"User-Agent": UserAgent().random}
    response = requests.get(url, headers=headers)
    encoding = response.encoding if response.encoding else 'utf-8'
    return response.content.decode(encoding, errors='ignore')


if __name__ == '__main__':
    for index in range(1, 4):
        triumph_base_url = f'https://www.triumph-motorcycles.com.vn/mo-to?page={index}&cats=&price=&sort='
        triumph_bikes_data = triumph_crawler(triumph_base_url)
        write_to_csv(triumph_bikes_data)
