from typing import Dict

from bs4 import BeautifulSoup

from postautomation import PostData
from postautomation.handlers.base import Handler


class E621Handler(Handler):
    def supports_domain(self, domain: str) -> bool:
        return domain == "e621.net"

    def scrape(self, url: str, document: BeautifulSoup) -> PostData:
        artist = str(document.find(
            "a",
            {"itemprop": "author"},
        ).contents[0]).replace(" (artist)", "")
        img_url = document.find(
            "section", {"id": "image-container"},
        )["data-file-url"]

        return PostData(
            url,
            None,
            artist,
            img_url
        )
