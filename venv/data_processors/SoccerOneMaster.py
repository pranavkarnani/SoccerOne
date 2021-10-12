# Creates the soccer one master file which contains references to all other csv's
# SoccerOneMaster.csv contains the player name, postion, fantasy premier league player ID and fifa ID
# One CSV that will fetch you records from every CSV that exists
import os
import re
import datetime
import pandas as pd


def get_date(filename):
    date_pattern = re.compile(r'\b(\d{2})-(\d{2})-(\d{4})\b')
    matched = date_pattern.search(filename)
    if not matched:
        return None
    m, d, y = map(int, matched.groups())
    return datetime.date(y, m, d)


def makeMaster():
    FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
    ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
    DATA_PATH = ROOT_DIR + '/data/'

    file_list = os.listdir(DATA_PATH)

    dates = (get_date(fn) for fn in file_list)
    dates = (d for d in dates if d is not None)
    last_date = max(dates)  # Getting the latest date
    last_date = last_date.strftime('%m-%d-%Y')
    latest_file = [fn for fn in file_list if last_date in fn]

    fifa = pd.read_csv(DATA_PATH+latest_file[0])
    fpl = pd.read_csv(DATA_PATH+'season_player_stats_df.csv')

    # fetches all fifa players with overall > 70
    fifa = fifa[fifa["Overal"] >= 70]

    # Inner join on name and club
    soccerOneDF = fifa.merge(fpl, how='inner', left_on=['Name', 'Club'], right_on=['fullname', 'Club'])
    soccerOneDF = soccerOneDF.rename({'ID': 'Fifa_ID'}, axis=1)
    soccerOneDF = soccerOneDF.rename({'id': 'Fpl_ID'}, axis=1)
    soccerOneDF = soccerOneDF.loc[:, ['Name', 'position', 'Club', 'Fifa_ID', 'Fpl_ID']]

    soccerOneDF.to_csv(DATA_PATH+'soccerOneMaster.csv')
