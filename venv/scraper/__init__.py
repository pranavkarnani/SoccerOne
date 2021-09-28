from twisted.internet import reactor
from twisted.internet import task

from scrapy.crawler import CrawlerRunner

from scraper.FifaSpider import FifaSpider
from scraper.PlayerURLSpider import PlayerSpider

import pandas as pd


def fifa_player_url_crawl():
    reactor.run()
    runner = CrawlerRunner({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    deferred = runner.crawl(PlayerSpider)
    deferred.addCallback(reactor.callLater, 5, run_crawl)
    return deferred


def fifa_player_stats_crawl():
    print('Spider for fifa rankings set up')
    reactor.run()
    runner = CrawlerRunner({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    deferred = runner.crawl(FifaSpider)
    deferred.addCallback(reactor.callLater, 5, run_crawl)
    return deferred
