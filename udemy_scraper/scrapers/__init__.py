import asyncio
from functools import reduce
from typing import List

from udemy_scraper.scrapers.subcategory_web_dev import UdemyWebDevelopment

api = UdemyWebDevelopment.create_url('Web+Development&')

if __name__ == '__main__':
    asyncio.run(UdemyWebDevelopment.run(UdemyWebDevelopment(), api))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(UdemyWebDevelopment.run(UdemyWebDevelopment(), api))


# class ScraperManager:
#     def __init__(self, UdemyWebDevelopment_enabled):
#         self.UdemyWebDevelopment_scraper = UdemyWebDevelopment(UdemyWebDevelopment_enabled)
#
#         self._scrapers = (self.UdemyWebDevelopment_scraper)
#
#     async def run(self) -> List:
#         """
#         Runs any enabled scrapers and returns a list of links
#         :return: list
#         """
#         urls = []
#         enabled_scrapers = self._enabled_scrapers()
#         if enabled_scrapers:
#             urls = reduce(
#                 list.__add__,
#                 await asyncio.gather(*map(lambda sc: sc.run(), enabled_scrapers)),
#             )
#         return urls
#
#     def _enabled_scrapers(self) -> List:
#         """
#         Returns a list of scrapers that should run
#         :return:
#         """
#         return list(filter(lambda sc: sc.should_run(), self._scrapers))
