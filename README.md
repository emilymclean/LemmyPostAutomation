# Lemmy Post Automation
A bot to automate regular image posts from a variety of sources.

## Running the Bot
In its default configuration, the bot is set up to accept links to image boards in a CSV list.
It then processes the list on a schedule defined using cron syntax, checks the target community 
for duplicates, and then posts the image (reuploaded to a provided hosting site) with a title in
the format of *Title [Content Warning] (Artist)*. Below is an example configuration setup to post
images from data/post_list.csv to transfem every day at 6am:

```python
import os

from plemmy import LemmyHttp

from postautomation import PostAutomation

if __name__ == "__main__":
    lemmy = LemmyHttp("https://lemmy.blahaj.zone")
    lemmy.login("username", "hunter2")
    automation = PostAutomation.create(
        lemmy,
        "transfem",
        "data/post_list.csv",
        "0 6 * * *"
    )
    automation.run()
```

From this, custom upload targets can be provided, as well as custom scrapers.