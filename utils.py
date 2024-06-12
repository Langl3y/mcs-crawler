import csv
import os
import requests

from fake_useragent import UserAgent


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
    try:
        headers = {"User-Agent": UserAgent().random}
        response = requests.get(url, headers=headers)
        encoding = response.encoding if response.encoding else 'utf-8'
    except Exception as e:
        raise e
    return response.content.decode(encoding, errors='ignore')