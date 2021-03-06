from abc import ABC, abstractmethod
from enum import Enum

class ScraperStates(Enum):
    DISABLED = "DISABLED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"


class BaseScraper(object):
    def __init__(self):
        super(BaseScraper, self).__init__()

        self._state = None
        self.scraper_name = None
        self.domain_name = "https://www.udemy.com/"
        self.pages_count = None
        self.current_page = 0

    # @abstractmethod
    # async def process(self):
    #     return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if any([s for s in ScraperStates if s.value == value]):
            self._state = value

    def set_state_disabled(self):
        self.state = ScraperStates.DISABLED.value
        print(f"{self.scraper_name} scraper disabled")

    def set_state_running(self):
        self.state = ScraperStates.RUNNING.value
        print(f"{self.scraper_name} scraper is running")

    def set_state_complete(self):
        self.state = ScraperStates.COMPLETE.value
        print(f"{self.scraper_name} scraper complete")

    def is_disabled(self):
        return self.state == ScraperStates.DISABLED.value

    def is_complete(self):
        return self.state == ScraperStates.COMPLETE.value

    def running(self):
        running = not self.is_disabled() and not self.is_complete()
        if running:
            self.set_state_running()
        return running

    def last_page_reached(self) -> bool:
        """
        Returns boolean of whether or not we should continue checking actual domain subcategory
        :return:
        """

        running = True

        if self.pages_count == self.current_page:
            print(f"Stopping loop. Reached the last page to scrape: {self.pages_count}")
            self.set_state_complete()

        return running
