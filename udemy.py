import re
from udemy_settings import *
from random import randint
import requests
import json
import time

from bs4 import BeautifulSoup as bs

KEY_WORD = "couponCode"
KEY_CHAR = "%"
KEY_EXPRESSION = "couponCode%3D"  # key word with ascii '3D' -> '=', from json file


def scrape_udemy(url):
    data = []

    # ORIGIN UDEMY PAGES COUNT
    for page in range(1, pages_count(url) + 1):

        start_time = time.time()

        print('--------------------------- PAGE ', page, ' --------------------------------')

        # if scrape_single_page(url.format(page)) :
        data.append(scrape_single_page(url.format(page)))

        time.sleep(randint(1, 5))

        # save data to file every 10 runs of loop
        if page % 10 == 0:
            f = open('courses.csv', 'w')
            f.write(str(data))
            f.close()

        print("--- {} seconds ---".format(time.time() - start_time))

    return data


def scrape_single_page(url):
    """ Scraping every of 16 courses from single page
        :return
    """
    data = []

    # scrape json of url
    page_format_json = get(url).json()

    num_of_items = len(page_format_json['unit']['items'])

    for item in range(num_of_items):
        # course title
        # data.append(page_format_json['unit']['items'][0 + item]['title'])

        time.sleep(randint(0, 2))

        # course link
        link = page_format_json['unit']['items'][0 + item]['url']

        course_link = 'https://www.udemy.com{}'.format(link)
        # print(full_link)
        if find_free_coupon(course_link) is not None:
            data.append(find_free_coupon(course_link))
        else:
            pass

    return data


def find_free_coupon(course_link):
    """ Find coupons in div as json
        :return link with already activated coupon
    """
    response = get(course_link)
    parsed_course = bs(response.content, 'lxml')  # maybe add if with response.status_code == 200

    working_coupon = None

    # dick key name -> "course_preview_path_w_return_link"
    # returns dick key value -> "dict_key_with_stored_coupon"
    dict_key_with_stored_coupon = convert_to_json(parsed_course)
    if dict_key_with_stored_coupon is not None:

        # looking for couponCode -> working or not
        if KEY_WORD in dict_key_with_stored_coupon:

            # extract coupon code from path
            coupon_name = dict_key_with_stored_coupon.partition(KEY_EXPRESSION)[2]

            # if string in not endswith couponCode=... (than delete string after '%')
            if KEY_CHAR in coupon_name:
                coupon_name = coupon_name.partition(KEY_CHAR)[0]

            url_with_attached_coupon = "{}?couponCode={}".format(course_link, coupon_name)
            print('PROMOTION (less than 100% off): ', url_with_attached_coupon)

            course_id = parsed_course.body.attrs['data-clp-course-id']

            api_url = "https://www.udemy.com/api-2.0/course-landing-components/{}" \
                      "/me/?components=buy_button,purchase,redeem_coupon,discount_expiration," \
                      "gift_this_course&discountCode={}".format(course_id, coupon_name)

            # print(api_url)

            api_resp = get(api_url).json()
            if api_resp["purchase"]["data"]["pricing_result"]["price"]["amount"] == 0:
                working_coupon = course_link
                print("Working coupon: ", working_coupon)

    else:

        raise Exception("Could not find coupon ! dict_key_with_stored_coupon is: "
                        , dict_key_with_stored_coupon)

        pass

    return working_coupon


def convert_to_json(parsed_course):
    """ Converting dirty div to proper json format """

    # div probably with coupon
    path = parsed_course.find('div', {'class': 'ud-component--course-landing-page-udlite--introduction-asset'})

    # Convert str(div) to json
    try:
        target_json_div = path['data-component-props']
        proper_json = json.loads(target_json_div)
        dict_key = proper_json['course_preview_path_w_return_link']
    except TypeError:
        dict_key = None

    return dict_key
