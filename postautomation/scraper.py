from typing import List
from urllib.parse import urlparse

import urllib3
from bs4 import BeautifulSoup

from postautomation import PostData
from postautomation.exceptions import NoMatchingHandler
from postautomation.handlers.base import Handler


class Scraper:
    handlers: List[Handler]

    def scrape(self, url: str) -> PostData:
        domain = urlparse(url).netloc
        try:
            handler = next(x for x in self.handlers if x.supports_domain(domain))
        except StopIteration:
            raise NoMatchingHandler()

        html = urllib3.request(
            "GET",
            url,
            headers={
                "Cookie": "; ".join([f"{k}={v}" for k,v in handler.setup_cookies().items()]),
                "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/31.0.1650.16 Safari/537.36"
            }
        ).data

        return handler.scrape(url, BeautifulSoup(html, features="html.parser"))
