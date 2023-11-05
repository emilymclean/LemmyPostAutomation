import os
from typing import Dict

from bs4 import BeautifulSoup

from postautomation import PostData
from postautomation.handlers.base import Handler


class FuraffinityHandler(Handler):

    def supports_domain(self, domain: str) -> bool:
        return domain == "furaffinity.net" or domain == "www.furaffinity.net"

    def setup_cookies(self) -> Dict[str, str]:
        return {
            "a": os.environ["furaffinity_a"],
            "b": os.environ["furaffinity_b"]
        }

    def scrape(self, url: str, document: BeautifulSoup) -> PostData:
        artist = document.find("meta", property="og:title")["content"].split(" by ")[1]
        img_container = document.find("img", {"id": "submissionImg"})
        img_url = "https:" + img_container["data-fullview-src"]
        title = img_container["alt"]

        return PostData(
            url,
            title,
            artist,
            img_url
        )
