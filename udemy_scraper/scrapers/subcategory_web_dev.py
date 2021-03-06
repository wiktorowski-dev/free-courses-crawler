from bs4 import BeautifulSoup
from udemy_scraper.scrapers.base_scraper import BaseScraper
from udemy_scraper.http_interaction import get_aiohttp, get_requests
from urllib.parse import urlencode
from typing import List
import requests

# FORMATTED API URL, FOR LATER USAGE
# params must be static, nno format here, format when acces to variable


###################################################


class UdemySubCatWebDevelopmentScraper(BaseScraper):

    def __init__(self, enabled):
        super(UdemySubCatWebDevelopmentScraper, self).__init__()
        self.scrapper_name = "Web Development"
        if not enabled:
            self.set_state_disabled()
        self.pages_count = None

    # @staticmethod
    # async def get_udemy_course_link(url) -> List:
    #     """
    #     Gets the udemy course link
    #     :param str url: The url to scrape data from
    #     :return: Coupon link of the udemy course
    #     """
    #     text = get_aiohttp(url)
    #     # print(text.json())
    #     return text

    @staticmethod
    def create_url():
        params = {
            "page_size": "16",
            "subcategory": 'Web Development',  # ! .format
            "instructional_level": "",
            "lang": "en",
            "price": "",
            "duration": "",
            "closed_captions": "",
            "category_id": "288",  # ! for every class, .format
            "source_page": "category_page",
            "locale": "pl_PL",
            "currency": "pln",
            "navigation_locale": "en_US",
            "skip_price": "False",
            "sos": "pc",
            "fl": "cat",
        }
        formatted = urlencode(params)
        template = "https://udemy.com/api-2.0/discovery-units/all_courses/?p={}&"
        url = template.format(1) + formatted
        return url


    @staticmethod
    def pages_count(url):

        """ Getting amount of pages from api """
        whole_json = get_requests(url).json()
        pagination = whole_json['unit']['pagination']['total_page']
        print(pagination)

        return pagination



# ud = udemy_cat_development.scrape_udemy(UDEMY_API_URL)


# TEACHINGUIDE_API_URL = "https://teachinguide.azure-api.net/course-coupon?sortCol=created_d&sortDir=DESC&length=100" \
#                        "&page={}&inkw=&discount=100&language=English&ignore=true&"
#
# teachgd = teachinguide_api.scrape_teachinguide(TEACHINGUIDE_API_URL)


# aa = udemy_cat_development.do_smth()

# promo = scrape_courses.scrape_pepper(url)

# szkolenia_kursy = scrape_courses.scrape_pepper_szkolenia_kursy()
# udemy = scrape_courses.scrape_pepper_udemy()


# urls = {'szkolenia i kursy': 'https://www.pepper.pl/grupa/szkolenia-i-kursy?page={}',
#         'uslugi i subskrypcje': 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}',
#         'udemy.com': 'https://www.pepper.pl/promocje/udemy.com?page={}'}

# szkolenia_kursy = scrape_courses.scrape_pepper(urls['szkolenia i kursy'])
#
# uslugi_subskrypcje = scrape_courses.scrape_pepper(urls['uslugi i subskrypcje'])
#
# udemy = scrape_courses.scrape_pepper(urls['udemy.com'])
