import re
import requests
from bs4 import BeautifulSoup as bs

# url_pepper = 'https://www.pepper.pl/grupa/internet-i-uslugi?page={}'
url_pepper = 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}'


# cookie = s.cookies.set("hide_expired=%221%22", "the cookie works",
#                        domain='https://www.pepper.pl/grupa/internet-i-uslugi')

# cookies = dict(cookies_are="hide_expired=%221%22")


def get(url):
    r = requests.get(url)
    return r


def post(url):
    r = requests.post(url)
    return r


def pages_count(response):
    soup = bs(response.text, 'html.parser')
    count = int(soup.find('span', {'class': re.compile('last-page')}).text)
    return count


def set_cookie():
    # turn off expired offers
    cookie_name = 'hide_expired'
    cookie_value = '%221%22'
    cookie = {cookie_name: cookie_value}
    return cookie


def scrape_pepper():
    pages = []

    s = requests.Session()
    s.headers.update({
                         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})
    s.get(url_pepper)

    cookie = s.get(url_pepper, cookies=set_cookie())

    # r = s.get(url_pepper.format(1))
    for page in range(pages_count(cookie)):
        page += 1
        # url = url_pepper.format(page)
        # resp = get(url)

        filtered_page = s.get(url_pepper.format(page), cookies=set_cookie())

        pages.append(find_free_offers(filtered_page))

    return pages


def find_free_offers(response):
    soup = bs(response.text, 'html.parser')
    articles = soup.find_all('div', {'class': 'threadGrid'})

    data = []

    # for one page
    for article in articles:
        # price
        # price = article.find('span', {'class': re.compile('thread-price')})
        # title = article.find('a', {'class': re.compile('thread-title')})
        # re_href = ".*https://www.pepper.pl/promocje/.*"
        title = article.find('a', href=re.compile(".*https://www.pepper.pl/promocje/.*"))

        # TODO: mam linki, teraz zrobic jakies dictionary do tego, dodac cene opisy, link, wypisywac nie wszystkie promocje
        #   a tylko te za darmo i jedynie kursy a nie wszystkie oferty


        # offer_description = article.find('div', {'class': re.compile('title')}).strong.a

        # price = article.find('span', {'class': re.compile('expired-threads')})

        # if price is not None:
        #     data.append(price)
        try:
            data.append(title['href'])
        except TypeError:
            pass


        # if offer_description is not None:
        #     data.append(offer_description.text)

    return data
