from PIL.Image import Image
from plemmy import LemmyHttp


class PostMonitor:
    community_name: str
    lemmy: LemmyHttp

    def __init__(self, community_name: str, lemmy: LemmyHttp):
        self.community_name = community_name
        self.lemmy = lemmy

    def update_database(self):

        pass

    def has_been_posted(self, image: Image) -> bool:
        return False
