from abc import ABC
from typing import Dict

from bs4 import BeautifulSoup

from src import PostCandidate


class Handler(ABC):

    def supports_domain(self, domain: str) -> bool:
        pass

    def setup_cookies(self) -> Dict[str, str]:
        return {}

    def scrape(self, url: str, document: BeautifulSoup) -> PostCandidate:
        pass
