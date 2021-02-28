import requests
from fake_useragent import UserAgent


def get(url):
    ua = UserAgent()
    headers = {
        "User-Agent": str(ua.chrome),
        "Accept-Language": "pl;q=0.7",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Connection": "keep-alive",
        'Cache-Control': 'private, max-age=0, no-cache'

    }
    r = requests.get(url, headers=headers)
    return r


def pages_count(url):
    whole_json = requests.get(url.format(1)).json()
    pagination = whole_json['unit']['pagination']['total_page']

    return pagination
