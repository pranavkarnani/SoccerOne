# File to get all data provided by the Fantasy Premier League's official website using an API
# Auto - scheduled fetcher which is invoked everyday at 1:30 PM

import pandas as pd
import numpy as np
import requests
from scraper.Fixtures import getFixtures
import os

# Used to get the full name of the player without the middle name
def refineName(name):
    nameBuffer = name.split(' ')
    if len(nameBuffer) > 2:
        return nameBuffer[0] + ' ' + nameBuffer[-1]
    else:
        # Returns the name if the player has just the first name
        return name


def getFantasyPL():
    # Initializing path to data directory
    FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
    ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH,'..'))
    DATA_PATH = ROOT_DIR + '/data/'

    # Fetching data from the below API
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = response.json()

    # Events - Games, stores game-week information
    events_json = data['events']
    # Teams - Stores all the teams and their strength
    teams_json = data['teams']
    # Season Player Stats - Contains detailed performance statistics of each player in the league
    season_player_stats_json = data['elements']
    # Element Types - Classifies player based on position - Forwards, Midfielders, Defenders, Goalkeepers
    element_types = data['element_types']

    # Creating a dictionary to store all the 4 Element Types with its ID and name
    player_pos = {}
    for item in element_types:
        player_pos[item['id']] = item['singular_name']
    player_pos_df = pd.DataFrame(player_pos.items(), columns=['position_id', 'position'])

    # Creating the events CSV
    event_data_columns = ["id", "name", "deadline_time", "finished"]
    events = []
    for json_object in events_json:
        item = []
        for column in event_data_columns:
            item.append(json_object[column])
        events.append(item)
    events_df = pd.DataFrame(events, columns=event_data_columns)
    events_df.to_csv(DATA_PATH+'events.csv')

    # Creating the teams csv
    team_data_columns = ["id", "code", "name", "short_name", "strength", "strength_overall_home",
                         "strength_overall_away",
                         "strength_attack_home", "strength_attack_away", "strength_defence_home",
                         "strength_defence_away"]
    teams = []
    for json_object in teams_json:
        item = []
        for column in team_data_columns:
            item.append(json_object[column])
        teams.append(item)

    # Maintaining integrity in team names to avoid problems while merging dataframes
    teams_df = pd.DataFrame(teams, columns=team_data_columns)
    teams_df['name'] = np.where(teams_df['name'] == 'Man City', 'Manchester City', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Man Utd', 'Manchester Utd', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Leicester', 'Leicester City', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Leeds', 'Leeds United', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Norwich', 'Norwich City', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Spurs', 'Tottenham', teams_df['name'])
    teams_df['name'] = np.where(teams_df['name'] == 'Newcastle', 'Newcastle Utd', teams_df['name'])
    teams_df = teams_df.rename({'name': 'Club'}, axis=1)
    teams_df.to_csv(DATA_PATH+'teams.csv')

    # Getting season fixtures and predicting complexity
    getFixtures()

    # Generating season player statistics dataframe and CSV
    season_player_stats_columns = ["chance_of_playing_next_round", "chance_of_playing_this_round", "code", "element_type",
                                   "ep_next", "ep_this", "event_points", "first_name", "form", "id", "news", "news_added",
                                   "now_cost", "points_per_game", "second_name", "selected_by_percent", "team_code",
                                   "total_points",
                                   "value_form", "value_season", "web_name", "minutes", "goals_scored", "assists",
                                   "clean_sheets", "goals_conceded", "own_goals", "penalties_saved", "penalties_missed",
                                   "yellow_cards", "red_cards", "saves", "bonus", "influence", "creativity", "threat",
                                   "ict_index", "influence_rank_type", "creativity_rank_type", "threat_rank_type",
                                   "ict_index_rank", "ict_index_rank_type", "penalties_order", "penalties_text"]
    season_player_stats = []
    for json_object in season_player_stats_json:
        item = []
        for column in season_player_stats_columns:
            item.append(json_object[column])
        season_player_stats.append(item)

    # Merging season player stats with position
    season_player_stats_df = pd.DataFrame(season_player_stats, columns=season_player_stats_columns)
    season_player_stats_df = season_player_stats_df.merge(player_pos_df, how='left', left_on=['element_type'],
                                                          right_on=['position_id'])

    season_player_stats_df = season_player_stats_df.merge(teams_df[['code', 'Club']],
                                                          how='left', left_on=['team_code'], right_on=['code'])

    season_player_stats_df['fullname'] = season_player_stats_df['first_name'] + ' ' + season_player_stats_df['second_name']
    season_player_stats_df['fullname'] = season_player_stats_df['fullname'].apply(refineName)
    season_player_stats_df.to_csv(DATA_PATH+'season_player_stats_df.csv')
