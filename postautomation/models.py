from dataclasses import dataclass
from typing import Optional, Dict, List

from pandas import DataFrame


@dataclass
class PostData:
    url: str
    title: Optional[str]
    artist: str
    image_url: str
    nsfw: bool
    content_warnings: Optional[List[str]] = None


@dataclass
class PostCandidate:
    url: str
    title: Optional[str]
    content_warnings: Optional[List[str]]

    @staticmethod
    def from_dataframe(df: Dict[str, str]):
        return PostCandidate(
            url=df["url"],
            title=df["title"] if "title" in df else None,
            content_warnings=df["content_warnings"].split(";") if "content_warnings" in df else None
        )
