from scraper.PlayerSpider import crawl_url

# Function driving crawler - invoked from main
def fifaCrawl():
    print('crawling')
    crawl_url()


def get_news():
    print("Getting news titles")
    get_news_titles()
