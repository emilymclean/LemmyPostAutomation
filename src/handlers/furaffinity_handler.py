import os
from typing import Dict

from bs4 import BeautifulSoup

from src import PostCandidate
from src.handlers.base import Handler


class FuraffinityHandler(Handler):

    def supports_domain(self, domain: str) -> bool:
        return domain == "furaffinity.net"

    def setup_cookies(self) -> Dict[str, str]:
        return {
            "a": os.environ["furaffinity_a"],
            "b": os.environ["furaffinity_b"]
        }

    def scrape(self, url: str, document: BeautifulSoup) -> PostCandidate:
        artist = document.find("meta", property="og:title")["content"].split(" by ")[1]
        img_container = document.find("img", {"id": "data-fullview-src"})
        img_url = img_container["data-fullview-src"]
        title = img_container["alt"]

        return PostCandidate(
            url,
            title,
            artist,
            img_url
        )
