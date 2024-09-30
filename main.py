import os

from pythonlemmy import LemmyHttp

from postautomation import PostAutomation

if __name__ == "__main__":
    lemmy = LemmyHttp(os.environ["instance"])

    if "username" in os.environ:
        lemmy.login(os.environ["username"], os.environ["password"])
    else:
        lemmy.set_jwt(os.environ["jwt"])

    automation = PostAutomation.create(
        lemmy,
        os.environ["community"],
        "data/post_list.csv",
        os.environ["schedule"]
    )
    automation.run()
