import traceback
from datetime import datetime
from io import BytesIO
from os import wait
from time import sleep
from typing import List, Optional

import requests
from PIL import Image
from croniter import croniter
from plemmy import LemmyHttp
from plemmy.responses import GetCommunityResponse

from postautomation import PostCandidate, PostData
from postautomation.candidate import CandidateProvider, CSVCandidateProvider
from postautomation.handlers.e621_handler import E621Handler
from postautomation.handlers.furaffinity_handler import FuraffinityHandler
from postautomation.monitor import PostMonitor
from postautomation.scraper import Scraper
from postautomation.uploader import Uploader, CatboxUploader


class PostAutomation:
    lemmy: LemmyHttp
    community_id: int
    monitor: PostMonitor
    scraper: Scraper
    candidate_provider: CandidateProvider
    cron: Optional[croniter]
    uploader: Uploader

    def __init__(
            self,
            lemmy: LemmyHttp,
            community_name: str, monitor:
            PostMonitor,
            scraper: Scraper,
            candidate_provider: CandidateProvider,
            uploader: Uploader,
            cron: Optional[str]
    ):
        self.lemmy = lemmy
        self.community_id = GetCommunityResponse(lemmy.get_community(name=community_name)).community_view.community.id
        self.monitor = monitor
        self.scraper = scraper
        self.candidate_provider = candidate_provider
        self.uploader = uploader
        if cron is not None:
            self.cron = croniter(cron, datetime.now())

    @staticmethod
    def create(lemmy: LemmyHttp, community_name: str, csv_file_location: str, cron: Optional[str] = None):
        return PostAutomation(
            lemmy,
            community_name,
            PostMonitor(community_name, lemmy),
            Scraper([E621Handler(), FuraffinityHandler()]),
            CSVCandidateProvider(csv_file_location),
            CatboxUploader(),
            cron
        )

    def run(self):
        if self.cron is None:
            return

        while True:
            next_run: datetime = self.cron.get_next(datetime)
            sleep_time = (next_run - datetime.now()).seconds
            print(f"Sleeping for {sleep_time}")
            sleep(sleep_time)
            self.run_once()

    def run_once(self):
        print("Updating database")
        self.monitor.update_database()

        print("Making a post")
        candidates: List[PostCandidate] = self.candidate_provider.list_candidates(None)[0]
        chosen: Optional[PostData] = None
        chosen_image: Optional[Image] = None
        for candidate in candidates:
            scraped = self.scraper.scrape(candidate.url)
            image = Image.open(BytesIO(requests.get(scraped.image_url).content))
            if not self.monitor.has_been_posted(image):
                if scraped.title is None:
                    scraped.title = candidate.title
                chosen = scraped
                chosen_image = image
                self.candidate_provider.remove_candidate(candidate)
                break

        if chosen is None:
            print("No candidates found")
            return

        print("Uploading image")
        try:
            image_url = self.uploader.upload(chosen.image_url, chosen_image)
        except Exception:
            print(traceback.format_exc())
            image_url = chosen.image_url

        self.lemmy.create_post(
            self.community_id,
            f"{chosen.title} ({chosen.artist})",
            f"[Source]({chosen.url})",
            nsfw=chosen.nsfw,
            url=image_url
        )