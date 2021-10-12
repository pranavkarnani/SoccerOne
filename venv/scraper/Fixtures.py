import requests
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os


# Function that fetches upcoming fixtures for this season
def getFixtures():

    # Initializing path to the data directory
    FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
    ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
    DATA_PATH = ROOT_DIR+'/data/'
    print('get fixtures')

    # Url containing all fixtures
    fixtures_url = 'https://cdn.bettingexpert.com/assets/England-Premier-League-fixture-2021-2022.csv'

    # Downloading csv file from the url
    req = requests.get(fixtures_url)
    url_content = req.content
    csv_file = open(DATA_PATH+'England-Premier-League-fixture-2021-2022.csv', 'wb')

    # Writing data to the CSV file
    csv_file.write(url_content)
    csv_file.close()
    gameday_nested = [(i, i, i, i, i, i, i, i, i, i) for i in range(1, 39)]
    gameday = [item for sublist in gameday_nested for item in sublist]

    df = pd.read_csv(DATA_PATH+'England-Premier-League-fixture-2021-2022.csv', sep=',', index_col=False)
    del df['League']
    df['Gameday'] = gameday
    df = df[['Gameday', 'Date', 'Home', 'Away']]
    df.set_index('Home', drop=True)

    team_data_df = pd.read_csv(DATA_PATH+'teams.csv', sep=',', index_col=1)

    del team_data_df['Unnamed: 0']
    del team_data_df['short_name']
    del team_data_df['strength']
    del team_data_df['strength_attack_home']
    del team_data_df['strength_attack_away']
    del team_data_df['strength_defence_home']
    del team_data_df['strength_defence_away']

    home_strength = dict(zip(team_data_df.Club, team_data_df.strength_overall_home))
    away_strength = dict(zip(team_data_df.Club, team_data_df.strength_overall_away))

    home_df = df['Home'].to_frame()
    away_df = df['Away'].to_frame()

    df['Home_Strength'] = df['Home'].map(home_strength)
    df['Away_Strength'] = df['Away'].map(away_strength)

    df['Home_Win'] = 100 * ((df['Home_Strength'] - np.min(df['Home_Strength'])) /
                            (np.max(df['Home_Strength']) - np.min(df['Home_Strength'])))

    df['Away_Win'] = 100 * ((df['Away_Strength'] - np.min(df['Away_Strength'])) /
                            (np.max(df['Away_Strength']) - np.min(df['Away_Strength'])))

    strength_comparison = np.where(df['Home_Win'] > df['Away_Win'], df['Home'], df['Away'])
    df['Predicted_Winning_Team'] = strength_comparison
    df['Home_Win'] = df['Home_Win'].round(2)
    df['Away_Win'] = df['Away_Win'].round(2)

    del df['Home_Strength']
    del df['Away_Strength']
    df.to_csv(DATA_PATH+'Fixtures_With_Win.csv', index=False)