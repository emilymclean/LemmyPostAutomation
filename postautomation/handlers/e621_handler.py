from typing import Dict

from bs4 import BeautifulSoup

from postautomation import PostCandidate
from postautomation.handlers.base import Handler


class E621Handler(Handler):
    def supports_domain(self, domain: str) -> bool:
        return domain == "e621.net"

    def scrape(self, url: str, document: BeautifulSoup) -> PostCandidate:
        artist = str(document.find(
            "a",
            {"itemprop": "author"},
        ).contents[0]).replace(" (artist)", "")
        img_url = document.find(
            "section", {"id": "image-container"},
        )["data-file-url"]

        return PostCandidate(
            url,
            None,
            artist,
            img_url
        )
