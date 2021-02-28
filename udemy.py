import re
from udemy_settings import *
import requests
import json
import time

from bs4 import BeautifulSoup as bs


def scrape_udemy(url):
    data = []

    # ORIGIN UDEMY PAGES COUNT
    for page in range(1, pages_count(url) + 1):
        time.sleep(30)

        # FOR TESTS ONLY
        # for page in range(1, 100):
        start_time = time.time()

        # single_page = get(url.format(page))
        # page_format_json = requests.get(url.format(page)).json()
        print('--------------------------- PAGE ', page, ' --------------------------------')
        # if scrape_single_page(url.format(page)):
        data.append(scrape_single_page(url.format(page)))
        if page % 10 == 0:
            f = open('courses.csv', 'w')
            f.write(str(data))
            f.close()

        # else:
        #     pass
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

        time.sleep(0.5)

        # course link
        link = page_format_json['unit']['items'][0 + item]['url']

        course_link = 'https://www.udemy.com{}'.format(link)
        # print(full_link)
        # if find_coupon(course_link) is not None:
        data.append(find_coupon(course_link))
        # else:
        #     pass

    return data


def find_coupon(course_link):
    """ Find coupons in div as json
        return: link with already activated coupon
    """
    response = get(course_link)

    parsed_course = bs(response.content, 'lxml')  # maybe add if with response.status_code == 200

    urls, api_urls, working_coupons = [], [], []

    # dick key name -> "course_preview_path_w_return_link"
    # returns dick key value -> "dict_key_with_stored_coupon"
    dict_key_with_stored_coupon = convert_to_json(parsed_course)

    key_word = "couponCode"

    # looking for couponCode -> working or not
    if key_word in dict_key_with_stored_coupon:

        # extract coupon code from path
        coupon_name = dict_key_with_stored_coupon.partition("couponCode%3D")[2]
        if '%' in coupon_name:
            coupon_name = coupon_name.partition('%')[0]


        # print("couponCode found in: ", full_link)
        # print(dict_key_with_stored_coupons)
        url_with_attached_coupon = "{}?couponCode={}".format(course_link, coupon_name)
        # urls.append(url_with_attached_coupon)
        print('LINK: ', url_with_attached_coupon)

        # try:
        course_id = parsed_course.body.attrs['data-clp-course-id']

        # except KeyError:
        #     pass
        api_url = "https://www.udemy.com/api-2.0/course-landing-components/{}" \
                  "/me/?components=buy_button,purchase,redeem_coupon,discount_expiration,gift_this_course&discountCode={}"\
                  .format(course_id, coupon_name)

        # print(api_url)

        api_resp = get(api_url).json()
        if api_resp["purchase"]["data"]["pricing_result"]["price"]["amount"] == 0:
            working_coupons.append(course_link)
            print("Finally found working coupon: ", working_coupons)

    else:
        # print("couponCode not found in: ", course_link)
        urls = None

    return working_coupons


def convert_to_json(soup):
    """ Converting dirty div to proper json format """

    # div probably with coupon
    path = soup.find('div', {'class': 'ud-component--course-landing-page-udlite--introduction-asset'})

    # Convert str(div) to json
    target_json_div = path['data-component-props']
    proper_json = json.loads(target_json_div)
    dict_key = proper_json['course_preview_path_w_return_link']

    return dict_key
