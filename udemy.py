import re
from udemy_settings import *
import requests

from bs4 import BeautifulSoup as bs


def scrape_udemy(url):

    data = []

    # ORIGIN UDEMY PAGES COUNT
    # for page in range(1, pages_count(url) + 1):

    # FOR TESTS ONLY
    for page in range(1, 5):
        # single_page = get(url.format(page))
        # page_format_json = requests.get(url.format(page)).json()

        data.append(scrape_single_page(url.format(page)))

        print(data[page - 1])

    return data


def scrape_single_page(url):
    data = []

    # scrape json of url
    page_format_json = get(url).json()

    num_of_items = len(page_format_json['unit']['items'])

    try:
        for item in range(num_of_items):
            # course title
            # data.append(page_format_json['unit']['items'][0 + item]['title'])

            # course link
            link = page_format_json['unit']['items'][0 + item]['url']

            data.append('https://www.udemy.com{}'.format(link))
    except IndexError:
        pass

    return data
