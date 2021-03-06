import asyncio
import httpx
from datetime import datetime
from bs4 import BeautifulSoup
from udemy_scraper.scrapers.base_scraper import BaseScraper
from udemy_scraper.http_interaction import get_aiohttp, get_requests
from urllib.parse import urlencode
from time import time, sleep
from typing import List
import requests

# FORMATTED API URL, FOR LATER USAGE
# params must be static, nno format here, format when acces to variable


###################################################
from udemy_settings import convert_to_json


class UdemyWebDevelopment(object):
    """
    Contains any logic related to scraping of data from udemy.com/development/Web+Development
    """
    # links = []

    def __init__(self, free_coupons=[], links=[]):
        super(UdemyWebDevelopment, self).__init__()
        self.free_coupons = free_coupons
        self.links = links

    async def run(self, url):

        for page in range(1, self.pages_count(url) + 1):
            try:
                self.get_links_from_page(url, page)
                await self.check_link(page)
                if page == self.pages_count(url):
                    self.save_to_file()
            except (IndexError, KeyError):
                continue

    def get_links_from_page(self, url, page):
        """ Scraping page and inside page, scraping all 16 courses
            :return list of courses links
         """

        page_format_json = get_requests(url.format(page)).json()

        num_of_items = len(page_format_json['unit']['items'])

        for item in range(num_of_items):
            link = page_format_json['unit']['items'][0 + item]['url']
            course_link = 'https://www.udemy.com{}'.format(link)
            self.links.append(course_link)
        # await asyncio.gather(*self.links)

        return self.links

    async def check_link(self, page):
        """
        Checking if provided link have free coupon and adding into list
        :param page, only for printing

        """
        start_time = time()
        print('PAGE', page)

        for link in range(len(self.links)):
            print(".", end=" ")
            course_link = self.links[link]
            # course_link = await self.links[i]
            if await self.find_coupon(course_link):
                self.free_coupons.append(self.find_coupon(course_link))

        print("\n{} seconds".format(time() - start_time))
        self.links.clear()

    async def find_coupon(self, course_link):
        """ Find coupons in div as json
            :return link with already activated coupon
        """
        async with httpx.AsyncClient() as client:
        # response = get_requests(course_link)
            response = await client.get(course_link)

        parsed_course = BeautifulSoup(response.content, 'lxml')  # maybe add if with response.status_code == 200

        # dick key name -> "course_preview_path_w_return_link"
        # returns dick key value -> "dict_key_with_stored_coupon"
        dict_key_with_stored_coupon = convert_to_json(parsed_course)

        if dict_key_with_stored_coupon is not None:
            # looking for couponCode -> working or not
            if "couponCode" in dict_key_with_stored_coupon:

                # extract coupon code from path
                # key word with ascii '3D' -> '=', from json file
                coupon_name = dict_key_with_stored_coupon.partition("couponCode%3D")[2]

                # if string in not endswith couponCode=... (than delete string after '%')
                if '%' in coupon_name:
                    coupon_name = coupon_name.partition('%')[0]

                return self.gather_free_coupon(course_link, coupon_name, parsed_course)
        else:
            pass

    @staticmethod
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
        api_resp = get_requests(api_url).json()

        discount = api_resp["purchase"]["data"]["pricing_result"]["discount_percent"]

        if discount != 100:
            print('\nPROMOTION - {}% off): '.format(discount), url_with_attached_coupon)

        if api_resp["purchase"]["data"]["pricing_result"]["price"]["amount"] == 0:
            working_coupon = url_with_attached_coupon
            print('\nFREE COURSE !!!): ', url_with_attached_coupon)

            return working_coupon

    @staticmethod
    def create_url(category):
        api_template = "https://udemy.com/api-2.0/discovery-units/all_courses/?"

        params = {
            "instructional_level": "",
            "lang": "en",
            "price": "",
            "duration": "",
            "closed_captions": "",
            "category_id": "288",
            "source_page": "category_page",
            "locale": "pl_PL",
            "currency": "pln",
            "navigation_locale": "en_US",
            "skip_price": "False",
            "sos": "pc",
            "fl": "cat",
        }
        formatted = urlencode(params)
        url = api_template + "p={}&" + f"page_size=16&subcategory={category}" + formatted

        return url

    @staticmethod
    def pages_count(url):
        """ Getting amount of pages from api """
        whole_json = get_requests(url.format(1)).json()
        # whole_json = get_aiohttp(url.format(1)).json()
        pagination = whole_json['unit']['pagination']['total_page']

        return pagination

    # SAVING LINKS FOR FREE COURSES INTO FILE  @TESTS
    def save_to_file(self):
        actual_date = datetime.today().strftime('%Y-%m-%d  %H:%M:%S').replace(':', '-')
        try:
            f = open('f_c {}.csv'.format(actual_date), 'w')
            s1 = '\n'.join(self.free_coupons)
            f.write(s1)
            f.close()
        except PermissionError:
            print("Excel is opened, its raise PermissionError, I know... weird")
