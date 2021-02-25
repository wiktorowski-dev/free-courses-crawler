import re
import requests
import inspect
from bs4 import BeautifulSoup as bs


# url_pepper = 'https://www.pepper.pl/grupa/internet-i-uslugi?page={}'
# url_pepper = 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}'
# urls = {'szkolenia i kursy': 'https://www.pepper.pl/grupa/szkolenia-i-kursy?page={}',
#         'uslugi i subskrypcje': 'https://www.pepper.pl/grupa/uslugi-i-subskrypcje?page={}',
#         'udemy.com': 'https://www.pepper.pl/promocje/udemy.com?page={}'}


# cookie = s.cookies.set("hide_expired=%221%22", "the cookie works",
#                        domain='https://www.pepper.pl/grupa/internet-i-uslugi')

# cookies = dict(cookies_are="hide_expired=%221%22")


def get(url):
    r = requests.get(url)
    return r



def pages_count(response):
    soup = bs(response.text, 'html.parser')

    try:
        count = int(soup.find('span', {'class': re.compile('last-page')}).text)
    except AttributeError:
        count = 1

    return count


def set_cookie():
    # turn off expired offers
    name = 'hide_expired'
    value = '%221%22'
    cookie = {name: value}
    return cookie


# def get_urls_data(s):
#     global data, cookies
#     for url in urls:
#         data = s.get(urls[url])
#         cookies = s.get(urls[url], cookies=set_cookie())
#
#     return data, cookies

# def uslugi():
#     return
#
# def szkolenia():
#     return
#
# def udemy():
#     return


def scrape_pepper(url):

    session = requests.Session()
    session.headers.update({
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})

    data = []

    # set cookie to disable expired offers for every endpoint
    expired_on = session.get(url, cookies=set_cookie())

    for page in range(1, pages_count(expired_on) + 1):
        filtered_page = session.get(url.format(page), cookies=set_cookie())

        data.append(find_free_offers(filtered_page))

    return data


# SCRAPE WHOLE SITE /promocje
# def scrape_pepper(url):
#
#     data = []
#
#
#     # set cookie to disable expired offers for every endpoint
#
#     ex = session().get(url, cookies=set_cookie())
#
#     for page in range(pages_count(ex)):
#         page += 1
#
#         filtered_page = session().get(url.format(page), cookies=set_cookie())
#
#         data.append(find_free_offers(filtered_page))
#         print(page)
#
#     return data


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
        title = article.find('a', href=re.compile("web|development|kursy|programowanie"))

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
