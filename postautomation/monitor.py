from io import BytesIO

import imagehash
import requests
from PIL import UnidentifiedImageError, Image
from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetPostsResponse, GetCommunityResponse

from postautomation.data import MonitorPersistence


class PostMonitor:
    community_name: str
    community_id: int
    lemmy: LemmyHttp
    monitor_persistence: MonitorPersistence

    def __init__(self,
                 community_name: str,
                 lemmy: LemmyHttp,
                 monitor_persistence: MonitorPersistence = MonitorPersistence()
                 ):
        self.community_name = community_name
        self.lemmy = lemmy
        self.monitor_persistence = monitor_persistence

        self.community_id = GetCommunityResponse(lemmy.get_community(name=community_name)).community_view.community.id

    def update_database(self):
        initial_page = current_page = self.monitor_persistence.get_current_page(self.community_name)
        prevent_backtracking = False
        while True:
            print(f"Scanning page {current_page}")
            response = GetPostsResponse(self.lemmy.get_posts(community_id=self.community_id, page=current_page, limit=10, sort="Old"))
            posts = response.posts

            # We've gone too far, backtrack
            if len(posts) == 0 and not prevent_backtracking:
                current_page -= 1
                continue

            for post in posts:
                prevent_backtracking = True
                post = post.post
                print(f"Processing {post.name} (url = {post.url})")
                if self.monitor_persistence.has_processed(post.id):
                    continue
                if post.url is None:
                    continue

                try:
                    image = Image.open(BytesIO(requests.get(post.url).content))
                except (UnidentifiedImageError, requests.exceptions.ConnectionError):
                    continue

                phash = str(imagehash.phash(image))

                self.monitor_persistence.record_phash(self.community_name, phash, post.url, post.id)

            if len(posts) < 10:
                break

            current_page += 1
        self.monitor_persistence.set_current_page(self.community_name, current_page)
        print(f"Scanned from page {initial_page} to {current_page}")

    def has_been_posted(self, image: Image) -> bool:
        phash = str(imagehash.phash(image))
        return self.monitor_persistence.phash_exists(self.community_name, phash)
