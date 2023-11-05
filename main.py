import os

from plemmy import LemmyHttp

from postautomation.automation import PostAutomation
from postautomation.candidate import CSVCandidateProvider
from postautomation.data.monitor_persistence import MonitorPersistence
from postautomation.handlers.e621_handler import E621Handler
from postautomation.handlers.furaffinity_handler import FuraffinityHandler
from postautomation.monitor import PostMonitor
from postautomation.scraper import Scraper

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

    pass
