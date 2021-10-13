# File: PlayerSpider.py
# Names: Jaison Jose, Neha Joshi, Pranav Karnani, Preet Jain
# Driver Code - Spiders, Scrapers, API Calls, CSV Download data source
# Imports - get fantasy premier league data - scraper.FantasyPL.py
#         - get player model class object - models.Player.py
#         - get latest news - scraper.News.py
#         - clean latest news - data_processors.NewsCleaner.News.py

import os
import scrapy
import time
import logging
import pandas as pd
import datetime as dt

from scraper.FantasyPL import getFantasyPL
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from itemloaders import ItemLoader
from models.Player import Player
from scraper.News import get_news_titles
from data_processors.NewsCleaner import clean_news

# Player Spider used to get all player attributes from the FIFA Index Website using Scrapy
class PlayerSpider(scrapy.Spider):
    name = "players"
    domain = "https://www.fifaindex.com/"

    # Start request url defined
    def start_requests(self):
        start_urls = [
            'https://www.fifaindex.com/players/?gender=0&league=13&order=desc'
        ]
        logging.log(logging.INFO, "Loading requests")
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Parsing the url to get the content in that page
    def parse(self, response, **kwargs):
        playerTable = (response.xpath(
            '//table[@class="table table-striped table-players"]/tbody/tr/td/figure[@class="player"]/a/@href').getall())
        print(playerTable)
        for player in playerTable:
            playerUrl = 'https://www.fifaindex.com' + player
            print(playerUrl)
            yield scrapy.Request(url=playerUrl, callback=self.parse_player)

        # Fetches the next page in url to tackle pagination
        try:
            time.sleep(0.25)
            nextPage = response.xpath("//a[contains(text(), 'Next Page')]/@href").get()
            yield scrapy.Request(response.urljoin(nextPage), callback=self.parse)
        except error:
            print(error)

    # Parses all the player attributes
    def parse_player(self, response):
        player = ItemLoader(item=Player())
        ID = str(response.url).split('/')[4]
        Name = response.xpath("//h1/text()").get().strip()
        Nationality = response.xpath("//h2//text()").getall()[-1].strip()
        Overall, Potential = response.xpath("//h5/span/span/text()").getall()
        Height = response.xpath(
            "//p[contains(text(), 'Height')]/span/span/text()").get().strip(" cm")
        Weight = response.xpath(
            "//p[contains(text(), 'Weight')]/span/span/text()").get().strip(" kg")
        PreferredFoot = response.xpath(
            "//p[contains(text(), 'Preferred Foot')]/span/text()").get()[0]
        BirthDate = response.xpath(
            "//p[contains(text(), 'Birth Date')]/span/text()").get()
        Age = response.xpath("//p[contains(text(), 'Age')]/span/text()").get()
        PreferredPositions = "/".join(response.xpath(
            "//p[contains(text(), 'Preferred Positions ')]/span/a/@title").getall())
        PlayerWorkRate = 'NA'
        PlayerWorkRateTemp = response.xpath(
            "//p[contains(text(), 'Player Work Rate')]/span/text()").get()

        # Handling null data
        if PlayerWorkRateTemp is not None:
            PlayerWorkRate.replace(" ", "")
        WeakFoot = str(len(response.xpath("//p[contains(text(), 'Weak Foot')]//i[contains(@class, 'fas')]")))
        SkillMoves = str(len(response.xpath("//p[contains(text(), 'Skill Moves')]//i[contains(@class, 'fas')]")))
        try:
            Value = 'NA'
            ValueTemp = response.xpath(
                "//p[contains(text(), 'Value')]/span[last()]/text()").get()
            if ValueTemp is not None:
                Value = ValueTemp.strip("€").replace(".", "")

            Wage = 'NA'
            WageTemp = response.xpath(
                "//p[contains(text(), 'Wage')]/span[last()]/text()").get()
            if WageTemp is not None:
                Wage = WageTemp.strip("€").replace(".", "")
            player.add_value("Value", Value)
            player.add_value("Wage", Wage)
        except e:
            pass

        player.add_value("ID", ID)
        player.add_value("Name", Name)
        player.add_value("Natinality", Nationality)
        player.add_value("Overal", Overall)
        player.add_value("Potential", Potential)
        player.add_value("Height", Height)
        player.add_value("Weight", Weight)
        player.add_value("PreferredFoot", PreferredFoot)
        player.add_value("BirthDate", BirthDate)
        player.add_value("Age", Age)
        player.add_value("PreferredPositions", PreferredPositions)
        player.add_value("PlayerWorkRate", PlayerWorkRate)
        player.add_value("WeakFoot", WeakFoot)
        player.add_value("SkillMoves", SkillMoves)

        try:
            Club = response.xpath("//div[h5/a/text()][div/p[4]]/h5/a/text()").get()
            Club_Position = response.xpath("//div[h5/a/text()][div/p[4]]/div/p[1]/span/a/@title").get()
            Club_KitNumber = response.xpath("//div[h5/a/text()][div/p[4]]/div/p[2]/span/text()").get()
            Club_JoinedClub = response.xpath("//div[h5/a/text()][div/p[4]]/div/p[3]/span/text()").get()
            Club_ContractLength = response.xpath("//div[h5/a/text()][div/p[4]]/div/p[4]/span/text()").get()

            if Club == "Tottenham Hotspur":
                Club = "Tottenham"
            elif Club == "Wolverhampton Wanderers":
                Club = "Wolves"
            elif Club == "West Ham United":
                Club = "West Ham"
            elif Club == "Brighton & Hove Albion":
                Club = "Brighton"

            player.add_value("Club", Club)
            player.add_value("Club_Position", Club_Position)
            player.add_value("Club_KitNumber", Club_KitNumber)
            player.add_value("Club_JoinedClub", Club_JoinedClub)
            player.add_value("Club_ContractLength", Club_ContractLength)
        except e:
            pass

        try:
            Nation = response.xpath("//div[h5/a/text()][count(div/p)=2]/h5/a/text()").get()
            Nation_Position = response.xpath("//div[h5/a/text()][count(div/p)=2]/div/p[1]/span/a/@title").get()
            Nation_KitNumber = response.xpath("//div[h5/a/text()][count(div/p)=2]/div/p[2]/span/text()").get()
            player.add_value("Nation", Nation)
            player.add_value("Nation_Position", Nation_Position)
            player.add_value("Nation_KitNumber", Nation_KitNumber)
        except e:
            pass

    # Fetches text based on response.xpath
        BallControl = response.xpath(
            "//p[contains(text(), 'Ball Control')]/span/span/text()").get()
        Dribbling = response.xpath(
            "//p[contains(text(), 'Dribbling')]/span/span/text()").get()

        Marking = response.xpath(
            "//p[contains(text(), 'Marking')]/span/span/text()").get()
        SlideTackle = response.xpath(
            "//p[contains(text(), 'Slide Tackle')]/span/span/text()").get()
        StandTackle = response.xpath(
            "//p[contains(text(), 'Stand Tackle')]/span/span/text()").get()

        Aggression = response.xpath(
            "//p[contains(text(), 'Aggression')]/span/span/text()").get()
        Reactions = response.xpath(
            "//p[contains(text(), 'Reactions')]/span/span/text()").get()
        AttPosition = response.xpath(
            "//p[contains(text(), 'Att. Position')]/span/span/text()").get()
        Interceptions = response.xpath(
            "//p[contains(text(), 'Interceptions')]/span/span/text()").get()
        Vision = response.xpath(
            "//p[contains(text(), 'Vision')]/span/span/text()").get()
        Composure = response.xpath(
            "//p[contains(text(), 'Composure')]/span/span/text()").get()

        Crossing = response.xpath(
            "//p[contains(text(), 'Crossing')]/span/span/text()").get()
        ShortPass = response.xpath(
            "//p[contains(text(), 'Short Pass')]/span/span/text()").get()
        LongPass = response.xpath(
            "//p[contains(text(), 'Long Pass')]/span/span/text()").get()

        Acceleration = response.xpath(
            "//p[contains(text(), 'Acceleration')]/span/span/text()").get()
        Stamina = response.xpath(
            "//p[contains(text(), 'Stamina')]/span/span/text()").get()
        Strength = response.xpath(
            "//p[contains(text(), 'Strength')]/span/span/text()").get()
        Balance = response.xpath(
            "//p[contains(text(), 'Balance')]/span/span/text()").get()
        SprintSpeed = response.xpath(
            "//p[contains(text(), 'Sprint Speed')]/span/span/text()").get()
        Agility = response.xpath(
            "//p[contains(text(), 'Agility')]/span/span/text()").get()
        Jumping = response.xpath(
            "//p[contains(text(), 'Jumping')]/span/span/text()").get()

        Heading = response.xpath(
            "//p[contains(text(), 'Heading')]/span/span/text()").get()
        ShotPower = response.xpath(
            "//p[contains(text(), 'Shot Power')]/span/span/text()").get()
        Finishing = response.xpath(
            "//p[contains(text(), 'Finishing')]/span/span/text()").get()
        LongShots = response.xpath(
            "//p[contains(text(), 'Long Shots')]/span/span/text()").get()
        Curve = response.xpath(
            "//p[contains(text(), 'Curve')]/span/span/text()").get()
        FKAcc = response.xpath(
            "//p[contains(text(), 'FK Acc.')]/span/span/text()").get()
        Penalties = response.xpath(
            "//p[contains(text(), 'Penalties')]/span/span/text()").get()
        Volleys = response.xpath(
            "//p[contains(text(), 'Volleys')]/span/span/text()").get()

        GKPositioning = response.xpath(
            "//p[contains(text(), 'GK Positioning')]/span/span/text()").get()
        GKDiving = response.xpath(
            "//p[contains(text(), 'GK Diving')]/span/span/text()").get()
        GKHandling = response.xpath(
            "//p[contains(text(), 'GK Handling')]/span/span/text()").get()
        GKKicking = response.xpath(
            "//p[contains(text(), 'GK Kicking')]/span/span/text()").get()
        GKReflexes = response.xpath(
            "//p[contains(text(), 'GK Reflexes')]/span/span/text()").get()

        Traits = "/".join(response.xpath(
            "//div[contains(h5/text(), 'Traits')]/div/p/text()").getall())
        Specialities = "/".join(response.xpath(
            "//div[contains(h5/text(), 'Specialities')]/div/p/text()").getall())

        # Adding attributes to the player object
        player.add_value("BallControl", BallControl)
        player.add_value("Dribbling", Dribbling)

        player.add_value("Marking", Marking)
        player.add_value("SlideTackle", SlideTackle)
        player.add_value("StandTackle", StandTackle)

        player.add_value("Aggression", Aggression)
        player.add_value("Reactions", Reactions)
        player.add_value("AttPosition", AttPosition)
        player.add_value("Interceptions", Interceptions)
        player.add_value("Vision", Vision)
        player.add_value("Composure", Composure)

        player.add_value("Crossing", Crossing)
        player.add_value("ShortPass", ShortPass)
        player.add_value("LongPass", LongPass)

        player.add_value("GKPositioning", GKPositioning)
        player.add_value("GKDiving", GKDiving)
        player.add_value("GKHandling", GKHandling)
        player.add_value("GKKicking", GKKicking)
        player.add_value("GKReflexes", GKReflexes)

        player.add_value("Acceleration", Acceleration)
        player.add_value("Stamina", Stamina)
        player.add_value("Strength", Strength)
        player.add_value("Balance", Balance)
        player.add_value("SprintSpeed", SprintSpeed)
        player.add_value("Agility", Agility)
        player.add_value("Jumping", Jumping)

        player.add_value("Heading", Heading)
        player.add_value("ShotPower", ShotPower)
        player.add_value("Finishing", Finishing)
        player.add_value("LongShots", LongShots)
        player.add_value("Curve", Curve)
        player.add_value("FKAcc", FKAcc)
        player.add_value("Penalties", Penalties)
        player.add_value("Volleys", Volleys)

        player.add_value("Traits", Traits)
        player.add_value("Specialities", Specialities)

        yield player.load_item()

# Crawl Job driver - Sets the spider settings
def crawl_job():
    settings = get_project_settings()
    date_time = dt.datetime.now().strftime("%m-%d-%Y")
    FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
    ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
    DATA_PATH = ROOT_DIR + '/data/'
    filename = DATA_PATH+'players-'+date_time+'.csv'
    runner = CrawlerRunner({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            "FEEDS": {
                filename: {"format": "csv"}
            }
        })
    return runner.crawl(PlayerSpider)


# Schedules the next crawl using twisted internet's reactor
def schedule_next_crawl(null, hour, minute):
    tomorrow = (
            dt.datetime.now() + dt.timedelta(days=1)
    ).replace(hour=hour, minute=minute, second=0, microsecond=0)
    sleep_time = (tomorrow - dt.datetime.now()).total_seconds()
    reactor.callLater(sleep_time, crawl_url)


# Driver function which fetches news, latest player season stats, updated player stats (fifa)
def crawl_url():
    getFantasyPL()
    get_news_titles()
    clean_news()
    configure_logging()
    print('crawling')
    d = crawl_job()
    # Adding callback at 1:30PM
    d.addCallback(schedule_next_crawl, hour=13, minute=30)
    d.addErrback(catch_error)
    reactor.run()


def catch_error(failure):
    print(failure.value)
