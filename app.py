import json
import time
from crawlers.kawa_crawler import kawa_crawler

with open('base_url.txt', 'r') as file:
    base_url = file.read()
    print('base url:', base_url)

with open('urls.json', 'r') as json_file:
    url = json.load(json_file)


def task_1():
    print("Task 1 is running")
    time.sleep(2)
    print("Task 1 is complete")


def task_2():
    print("Task 2 is running")
    time.sleep(2)
    print("Task 2 is complete")


if __name__ == '__main__':
    kawa_crawler()
