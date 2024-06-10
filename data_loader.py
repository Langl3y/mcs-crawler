# -*- coding: utf-8 -*-
import logging
import json
import os
import time

from models import session, Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

odoo_url = 'https://uit-acct5123-o21-cttt.odoo.com/web/login'
product_page = 'https://uit-acct5123-o21-cttt.odoo.com/odoo/products'
user = '19521497@gm.uit.edu.vn'
password = 'eriri123'

with open('configs/odoo_config.json', 'r') as file:
    odoo_config = json.load(file)


def login(driver):
    driver.get(odoo_url)
    user_template = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['user']))
    )
    password_template = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['password']))
    )
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['login_button']))
    )

    try:
        user_template.clear()
        user_template.send_keys(user)
        password_template.clear()
        password_template.send_keys(password)
    except Exception as e:
        logging.error(e)

    login_btn.click()

    time.sleep(5)
    try:
        print('product page url', product_page)
        driver.get('https://uit-acct5123-o21-cttt.odoo.com/odoo/products')
    except Exception as e:
        logging.error(e)

    load_products(driver)


def add_product(bike_info):
    bname = bike_info['name']
    bprice = bike_info['price']
    bmanu = bike_info['manufacturer']
    btax = bike_info['tax']

    product_name_template = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['product_name']))
    )
    product_price_template = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['product_price']))
    )
    product_tax_template = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, odoo_config['product_tax_template']))
    )

    bfullname = bmanu + ' ' + bname
    product_name_template.clear()
    product_name_template.send_keys(bfullname)

    product_price_template.clear()
    product_price_template.send_keys(bprice)
    time.sleep(2)

    return


def load_products(driver):
    products = session.query(Product).all()
    new_product_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, odoo_config['new_product']))
    )
    driver.execute_script("arguments[0].click();", new_product_btn)

    for product in products:
        new_product_loop_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, odoo_config['new_product_loop']))
        )
        driver.execute_script("arguments[0].click();", new_product_loop_btn)

        product_info = {
            'name': str(product.name),
            'price': str(product.price),
            'manufacturer': str(product.manufacturer),
            'tax': str(product.tax)
        }
        print('product info: ', product_info)
        add_product(product_info)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    login(driver)
