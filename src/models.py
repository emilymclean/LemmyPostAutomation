from dataclasses import dataclass
from tkinter import Image
from typing import Optional


@dataclass
class PostCandidate:
    url: str
    title: Optional[str]
    artist: str
    image_url: str
