from udemy_settings import *
from time import time


def scrape_teachinguide(url):
    """ API of teachinguide.com, stored many udemy coupons, filter=free
        (this is made for validation tests only)
        (also in future can be used for discord bot/discord integration)

        :return every link for free course with enrolled coupon
     """

    # for page in range(1, tg_pages_count(url) + 1):
    for page in range(tg_pages_count(url) + 1):
        get_links(page, url)
        print(get_links(page, url))


def get_links(page, url):
    start_time = time()  # timing start
    print('--------------------------- PAGE ', page, ' --------------------------------')

    page_format_json = get(url.format(page)).json()
    num_of_items = len(page_format_json['results'])
    for item in range(num_of_items):
        link = page_format_json['results'][item]['CouponLink']
        print(link)
    print("\n{} seconds".format(time() - start_time))  # timing end