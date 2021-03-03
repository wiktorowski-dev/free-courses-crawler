import requests
import json
from fake_useragent import UserAgent


def get(url):
    ua = UserAgent()
    headers = {
        "User-Agent": str(ua.chrome),
        "Accept-Language": "pl;q=0.7",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Connection": "keep-alive",
        # 'Content-Type': "text/plain"

    }
    r = requests.get(url, headers=headers)
    return r


def pages_count(url):
    """ Getting amount of pages from api """
    whole_json = get(url.format(1)).json()
    pagination = whole_json['unit']['pagination']['total_page']

    return pagination


def tg_pages_count(url):
    """ Getting amount of pages from api """
    whole_json = get(url.format(1)).json()
    pagination = whole_json['pages']

    return pagination


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
