from dataclasses import dataclass
from typing import Optional, Dict

from pandas import DataFrame


@dataclass
class PostData:
    url: str
    title: Optional[str]
    artist: str
    image_url: str
    nsfw: bool


@dataclass
class PostCandidate:
    url: str
    title: Optional[str]

    @staticmethod
    def from_dataframe(df: Dict[str, str]):
        return PostCandidate(
            url=df["url"],
            title=df["title"] if "title" in df else None
        )
