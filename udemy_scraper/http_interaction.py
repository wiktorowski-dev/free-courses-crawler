import aiohttp
import requests
from fake_useragent import UserAgent


async def get_aiohttp(url):
    """
    Send GET request to the url passed in
    :param url: The Url to get call get request on
    :return: data if any exists
    """
    ua = UserAgent()
    headers = {
        "User-Agent": str(ua.chrome),
        "Accept-Language": "pl;q=0.7",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Connection": "keep-alive",
        # 'Content-Type': "application/json"
    }
    try:
        async with aiohttp.ClientSession as session:
            async with session.get(url, headers=headers) as response:
                text = await response.read()
                return text
                # print(await response.json())
    except Exception as e:
        print(f"Error in get request: {e}")


def get_requests(url):
    ua = UserAgent()
    headers = {
        "User-Agent": str(ua.chrome),
        "Accept-Language": "pl;q=0.7",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Connection": "keep-alive",
        # 'Content-Type': "application/json"

    }
    with requests.get(url, headers) as request:
        return request
