import re
from udemy_settings import *
import requests
import json
import time

from bs4 import BeautifulSoup as bs


def scrape_udemy(url):
    data = []

    # ORIGIN UDEMY PAGES COUNT
    # for page in range(1, pages_count(url) + 1):

    # FOR TESTS ONLY
    for page in range(1, 10):
        start_time = time.time()

        # single_page = get(url.format(page))
        # page_format_json = requests.get(url.format(page)).json()
        print('--------------------------- PAGE ', page, ' --------------------------------')
        if scrape_single_page(url.format(page)) is not None:
            data.append(scrape_single_page(url.format(page)))
        else:
            pass
        print("--- %s seconds ---" % (time.time() - start_time))


        # try:
        #     print(data[page])
        # except IndexError:
        #     pass

    return data


def scrape_single_page(url):
    data = []

    # scrape json of url
    page_format_json = get(url).json()

    num_of_items = len(page_format_json['unit']['items'])

    for item in range(num_of_items):
        # course title
        # data.append(page_format_json['unit']['items'][0 + item]['title'])

        # course link
        link = page_format_json['unit']['items'][0 + item]['url']

        full_link = 'https://www.udemy.com{}'.format(link)
        # print(full_link)
        if find_coupon(full_link) is not None:
            data.append(find_coupon(full_link))
        else:
            pass

    return data


def find_coupon(full_link):
    r = requests.get(full_link)
    soup = bs(r.text, 'lxml')
    div_probably_with_coupon = soup.find('div',
                                         {'class': 'ud-component--course-landing-page-udlite--introduction-asset'})
    # load str(div) to json
    try:

        target_json_div = div_probably_with_coupon['data-component-props']
        proper_json = json.loads(target_json_div)

        dict_key_with_stored_coupons = proper_json['course_preview_path_w_return_link']

        # TODO znalezc w stringu substring 'couponCode' jezeli jest: data.append, else: pass
        if "couponCode" in dict_key_with_stored_coupons:

            data = ('LINK : ' + full_link + ' COUPON: ' + dict_key_with_stored_coupons)
            # print("couponCode found in: ", full_link)
            # print(dict_key_with_stored_coupons)

        else:
            # print("couponCode not found in: ", full_link)
            data = None
            pass

        return data
    except TypeError:
        pass
