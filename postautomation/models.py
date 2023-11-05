from dataclasses import dataclass
from typing import Optional


@dataclass
class PostData:
    url: str
    title: Optional[str]
    artist: str
    image_url: str


@dataclass
class PostCandidate:
    url: str
    title: Optional[str]
