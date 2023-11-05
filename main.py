from postautomation.handlers.e621_handler import E621Handler
from postautomation.handlers.furaffinity_handler import FuraffinityHandler
from postautomation.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    scraper.handlers = [E621Handler(), FuraffinityHandler()]
    print(scraper.scrape("https://e621.net/posts/4299268?q=trans_woman_%28lore%29+score%3A%3E2"))
