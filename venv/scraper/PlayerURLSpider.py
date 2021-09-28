import scrapy
import time
from scrapy.crawler import CrawlerProcess
import pandas as pd

player_url_list = []
class PlayerSpider(scrapy.Spider):
    name = "players"
    domain = "https://www.fifaindex.com/"

    def start_requests(self):
        urls = [
            'https://www.fifaindex.com/players/fifa21_486/?gender=0&league=13&order=desc'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        playerTable = (response.xpath(
            '//table[@class="table table-striped table-players"]/tbody/tr/td/figure[@class="player"]/a/@href').getall())

        for players in playerTable:
            playerUrl = 'https://www.fifaindex.com' + players
            player_list.append(playerUrl)

        try:
            print('check')
            time.sleep(0.25)
            nextPage = response.xpath("//a[contains(text(), 'Next Page')]/@href").get()
            print(nextPage)
            yield scrapy.Request(response.urljoin(nextPage), callback=self.parse)
        except:
            print('except')
            pass