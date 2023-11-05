from PIL.Image import Image

from postautomation.uploader import Uploader


class RawUploader(Uploader):

    def upload(self, url: str, image: Image) -> str:
        return url