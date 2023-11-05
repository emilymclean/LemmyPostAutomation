import os

from plemmy import LemmyHttp

from postautomation.automation import PostAutomation

if __name__ == "__main__":
    lemmy = LemmyHttp(os.environ["instance"])
    lemmy.login(os.environ["username"], os.environ["password"])
    automation = PostAutomation.create(
        lemmy,
        os.environ["community"],
        "data/post_list.csv",
        os.environ["schedule"]
    )
    automation.run()
