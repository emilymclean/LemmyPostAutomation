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
            mime = "image/jpeg"
        except OSError:
            image.save(b, "png")
            mime = "image/png"

        result = requests.post(self.api_base, data={
            "reqtype": "fileupload",
        }, files={
            "fileToUpload": (f"image.{mime.split('/')[1]}", b.getvalue(), mime)
        })

        content = result.content.decode("utf-8")
        if not content.startswith("http"):
            raise OSError(content)
        print(f"Image uploaded @ {content}")
        return content
