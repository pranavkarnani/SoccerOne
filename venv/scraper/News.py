# File - fetches all news with query as Premier League from Google News using beautiful soup
# Auto - scheduled scraper which is invoked everyday at 1:30 PM

import os
import requests
import datetime
import random
from bs4 import BeautifulSoup
import pandas as pd

from bs4 import BeautifulSoup
import requests, urllib.parse, lxml

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'


def paginate(url, previous_url=None):
    # Break from infinite recursion
    if url == previous_url: return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # First page
    yield soup

    next_page_node = soup.select_one('a#pnnext')

    # Stop when there is no next page
    if next_page_node is None: return

    next_page_url = urllib.parse.urljoin('https://www.google.com/', next_page_node['href'])

    # Pages after the first one
    yield from paginate(next_page_url, url)


def get_news_titles():
    # Gets all pages
    pages = paginate("https://www.google.com/search?hl=en-US&q=premierleague&tbm=nws")
    newsTitles = []
    for soup in pages:
        print(f'Current page: {int(soup.select_one(".YyVfkd").text)}\n')
        # Finding all headlines
        for result in soup.find_all("div", attrs={"role": "heading"}):
            newsTitles.append(result.text)

    # Converting to dataframe and adding a new CSV
    news = pd.DataFrame({"news": newsTitles})
    news.to_csv(DATA_PATH + "news.csv")
