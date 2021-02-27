import requests


def get(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Accept-Language": "pl;q=0.7"}
    r = requests.get(url, headers=headers)
    return r


def pages_count(url):
    whole_json = requests.get(url.format(1)).json()
    pagination = whole_json['unit']['pagination']['total_page']

    return pagination
