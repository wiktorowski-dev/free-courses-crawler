from datetime import datetime
from time import time

from bs4 import BeautifulSoup

from udemy_settings import *

KEY_WORD = "couponCode"
KEY_CHAR = "%"
KEY_EXPRESSION = "couponCode%3D"  # key word with ascii '3D' -> '=', from json file

free_coupons = []
# items = []


def scrape_udemy(url):
    """ Scraping page and inside page, scraping all 16 courses
        :return list of free courses links
     """

    # ORIGIN UDEMY PAGES COUNT
    for page in range(1, pages_count(url) + 1):

        start_time = time()
        print('--------------------------- PAGE ', page, ' --------------------------------')
        # sleep(randint(1, 5))

        page_format_json = get(url.format(page)).json()

        num_of_items = len(page_format_json['unit']['items'])

        f = open('items.csv', 'w')
        s1 = '\n'.join(free_coupons)
        f.write(s1)
        f.close()

        actual_date = datetime.today().strftime('%Y-%m-%d  %H:%M:%S').replace(':', '-')

        if page == pages_count(url):
            f1 = open('f_c {}.csv'.format(actual_date), 'w')
            s1 = '\n'.join(free_coupons)
            f1.write(s1)
            f1.close()

        # items.clear()

        save_to_file()

        for item in range(num_of_items):
            link = page_format_json['unit']['items'][0 + item]['url']
            course_link = 'https://www.udemy.com{}'.format(link)

            "TESTS FOR COURSES ADDED AND UPDATE TIME"
            # created_raw = page_format_json['unit']['items'][0 + item]['created']
            # creaeted = created_raw.replace('T', '  ').replace('Z', '')
            #
            # print("Created: ", creaeted)
            # last_update_date = page_format_json['unit']['items'][0 + item]['last_update_date']
            # print("Last update date: ", last_update_date, course_link, '\n')

            # items.append(course_link)

            if find_coupon(course_link):
                free_coupons.append(find_coupon(course_link))
            # check_and_append(course_link)

            print(".", end=" ")

        print("\n{} seconds".format(time() - start_time))

    return free_coupons


def save_to_file():
    try:
        f = open('raw-courses.csv', 'w')
        s1 = '\n'.join(free_coupons)
        f.write(s1)
        f.close()
    except PermissionError:
        print("Excel, close it u dumb !")


def find_coupon(course_link):
    """ Find coupons in div as json
        :return link with already activated coupon
    """
    response = get(course_link)
    parsed_course = BeautifulSoup(response.content, 'lxml')  # maybe add if with response.status_code == 200

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

            return gather_free_coupon(course_link, coupon_name, parsed_course)
    else:
        pass


def gather_free_coupon(course_link, coupon_name, parsed_course):
    """ Find coupon with price 100% off
        :return link for free udemy course
    """
    url_with_attached_coupon = "{}?couponCode={}".format(course_link, coupon_name)

    course_id = parsed_course.body.attrs['data-clp-course-id']

    api_url = "https://www.udemy.com/api-2.0/course-landing-components/{}" \
              "/me/?components=buy_button,purchase,redeem_coupon,discount_expiration," \
              "gift_this_course&discountCode={}".format(course_id, coupon_name)

    # API response with information about coupon (expired, working, price)
    api_resp = get(api_url).json()

    discount = api_resp["purchase"]["data"]["pricing_result"]["discount_percent"]
    code = api_resp["purchase"]["data"]["pricing_result"]["code"]
    classic_code = "KEEPLEARNING"

    if discount != 100 and code != classic_code:
        print('\nPROMOTION - {}% off): '.format(discount), url_with_attached_coupon)

    else:
        print('\nPROMOTION CODE EXPIRED/INVALID): ', url_with_attached_coupon)

    if api_resp["purchase"]["data"]["pricing_result"]["price"]["amount"] == 0:
        working_coupon = url_with_attached_coupon
        print('\nFREE COURSE !!!): ', url_with_attached_coupon)

        return working_coupon

