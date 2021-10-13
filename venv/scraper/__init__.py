# File: init.py
# Names: Jaison Jose, Neha Joshi, Pranav Karnani, Preet Jain
# Driver Code - Spiders
# Imports - crawl_url function from scraper.PlayerSpider.py, fetches all the data from various websites

from scraper.PlayerSpider import crawl_url

# Function driving crawler - invoked from main
def fifaCrawl():
    print('crawling')
    crawl_url()


def get_news():
    print("Getting news titles")
    get_news_titles()
