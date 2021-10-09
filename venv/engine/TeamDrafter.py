import os
import pandas as pd
import datetime

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'


def get_date(filename):
    date_pattern = re.compile(r'\b(\d{2})-(\d{2})-(\d{4})\b')
    matched = date_pattern.search(filename)
    if not matched:
        return None
    m, d, y = map(int, matched.groups())
    return datetime.date(y, m, d)


def get_file():
    file_list = os.listdir(DATA_PATH)
    dates = (get_date(fn) for fn in file_list)
    dates = (d for d in dates if d is not None)
    last_date = max(dates)  # Getting the latest date
    last_date = last_date.strftime('%m-%d-%Y')
    latest_file = [fn for fn in file_list if last_date in fn]
    return latest_file[0]


fifa = pd.read_csv(get_file())
soccerOne = pd.read_csv(DATA_PATH + 'soccerOneMaster.csv')
fpl = pd.read_csv(DATA_PATH + 'season_player_stats_df.csv')

