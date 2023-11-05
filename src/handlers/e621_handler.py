from typing import Dict

from bs4 import BeautifulSoup

from src import PostCandidate
from src.handlers.base import Handler


class E621Handler(Handler):
    def supports_domain(self, domain: str) -> bool:
        return domain == "e621.net"

    def scrape(self, url: str, document: BeautifulSoup) -> PostCandidate:
        artist = str(document.find(
            "a",
            {"itemprop": "author"},
        ).contents)
        img_url = document.find(
            "meta", property="og:image"
        )["content"].replace("/sample","")

        return PostCandidate(
            url,
            None,
            artist,
            img_url
        )
    