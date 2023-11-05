import io

import requests
from PIL.Image import Image

from postautomation.uploader import Uploader


class CatboxUploader(Uploader):
    api_base = "https://catbox.moe/user/api.php"

    def upload(self, url: str, image: Image) -> str:
        b = io.BytesIO()
        try:
            image.save(b, "jpeg")
        except OSError:
            image.save(b, "png")
        result = requests.post(self.api_base, files={
            "reqtype": "fileupload",
            "fileToUpload": b.getvalue()
        })

        print(result.content)
        return ""