from scraper.PlayerSpider import crawl_url
from scraper.News import get_news_titles


def fifaCrawl():
    get_news()
    print('crawling')
    crawl_url()


def get_news():
    print("Getting news titles")
    get_news_titles()
