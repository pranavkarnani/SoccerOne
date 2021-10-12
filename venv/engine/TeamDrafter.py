import os
import re

import numpy as np
import pandas as pd
import datetime

# Setting data path
FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'
pd.options.mode.chained_assignment = None  # default='warn'


# Gets the latest file name
def get_date(filename):
    date_pattern = re.compile(r'\b(\d{2})-(\d{2})-(\d{4})\b')
    matched = date_pattern.search(filename)
    if not matched:
        return None
    m, d, y = map(int, matched.groups())
    return datetime.date(y, m, d)


# Retrieves the player states file
def get_file():
    file_list = os.listdir(DATA_PATH)
    dates = (get_date(fn) for fn in file_list)
    dates = (d for d in dates if d is not None)
    last_date = max(dates)  # Getting the latest date
    last_date = last_date.strftime('%m-%d-%Y')
    latest_file = [fn for fn in file_list if last_date in fn]
    return latest_file[0]


# Driver function which selects a set of maximum 80 players out of 400+ players
def make_team():
    soccerOne = pd.read_csv(DATA_PATH + 'soccerOneMaster.csv', index_col=0)
    fwds = analyze(soccerOne[soccerOne['position'] == 'Forward'], 'Forward')
    mids = analyze(soccerOne[soccerOne['position'] == 'Midfielder'], 'Midfielder')
    defs = analyze(soccerOne[soccerOne['position'] == 'Defender'], 'Defender')
    goalies = analyze(soccerOne[soccerOne['position'] == 'Goalkeeper'], 'Goalkeeper')
    return fwds, mids, defs, goalies


# Analyzes players based on a variety of metrics including player form, season value, expected points etc
def analyze(players, player_type):
    fpl = pd.read_csv(DATA_PATH + 'season_player_stats_df.csv', index_col=0)
    player_attr = fpl.copy()
    metrics = []

    # Defining player metrics for forwards
    if player_type == "Forward":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'minutes', 'threat',
                   'total_points',
                   'selected_by_percent', 'ict_index', 'goals_scored', 'assists', 'form', 'value_season', 'news',
                   'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]
    # Defining player metrics for midfielders
    elif player_type == "Midfielder":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'selected_by_percent',
                   'total_points',
                   'minutes', 'threat', 'ict_index', 'influence', 'creativity', 'assists', 'form', 'value_season',
                   'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]
    # Defining player metrics for defenders
    elif player_type == "Defender":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'minutes', 'selected_by_percent',
                   'total_points',
                   'ict_index', 'clean_sheets', 'assists', 'form', 'value_season', 'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]
    # Defining player metrics for Goalkeepers
    elif player_type == "Goalkeeper":
        metrics = ['id', 'ep_this', 'points_per_game', 'selected_by_percent', 'chance_of_playing_this_round',
                   'total_points', 'ict_index',
                   'clean_sheets', 'saves', 'form', 'value_season', 'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]
    # Merging player from Soccer One dataset with their attributes fetched from Fantasy PL official website
    selection_metrics = players.loc[:, ['Name', 'position', 'Club', 'Fpl_ID', 'Fifa_ID']].merge(player_attr,
                                                                                                how="left",
                                                                                                left_on='Fpl_ID',
                                                                                                right_on='id')
    # Amount of money provided
    cost = 100
    selection_metrics = selection_metrics[selection_metrics['chance_of_playing_this_round'] != 0]
    # Normalizing cost of each player
    selection_metrics['now_cost'] = selection_metrics['now_cost'] / 10
    # Adding weights to parameters
    selection_metrics['total_points'] = selection_metrics['total_points'] * 2
    selection_metrics['selected_by_percent'] = selection_metrics['selected_by_percent'] * 2
    selection_metrics['value_season'] = selection_metrics['value_season'] * 1.2

    # Calculates Z-Scores to find the best players i.e. detect outliers
    normalized_players = compute_score(selection_metrics, metrics)

    # Creating an aggregate metric which fetches the best players in each segment
    normalized_players['aggregate'] = normalized_players.loc[:,
                                      [col for col in normalized_players.columns if 'soccer_one_' in col]].sum(axis=1)
    normalized_players['aggregate'] = normalized_players['aggregate'] / len(metrics)
    normalized_players = normalized_players[normalized_players['aggregate'] > 0]
    # Creating players that are efficient - Most points per unit cost
    normalized_players['efficiency'] = normalized_players['aggregate'] / normalized_players['now_cost']
    # Sorting data frame based on aggregate, efficiency and cost
    normalized_players = normalized_players.sort_values(by=['aggregate', 'efficiency', 'now_cost'], ascending=False)

    # Analyzing top 20 players
    players_to_analyze = 20
    if len(normalized_players) <= 20:
        players_to_analyze = len(normalized_players)

    normalized_players = normalized_players.sort_values(
        by='aggregate', ascending=False).reset_index().drop(["index"], axis=1)
    # Status stores the player selection status
    normalized_players['status'] = 0
    normalized_players = normalized_players.head(players_to_analyze)
    # Returns the list of top 20 players - visualized in main_menu.py
    return normalized_players

# Cost wrapper function called by the main_menu file to fetch the top 15 players required in the team
def cost_wrapper(players, player_type):
    cost = 100
    # Fetches the best 3 forwards that can be bought for $21
    if player_type == "Forward":
        selected = cost_analysis(players, 21, 3)
        cost -= np.sum(selected['now_cost'])
        return selected

    # Fetches the best 2 goalkeepers that can be bought for $11
    elif player_type == "Goalkeeper":
        selected = cost_analysis(players, 11, 2)
        cost -= np.sum(selected['now_cost'])
        return selected

    # Fetches the best 5 defenders that can be bought for $28
    elif player_type == "Defender":
        selected = cost_analysis(players, 28, 5, player_type)
        cost -= np.sum(selected['now_cost'])
        return selected

    # Fetches the best 5 midfielders that can be bought for $40
    elif player_type == "Midfielder":
        selected = cost_analysis(players, 40, 5, player_type)
        cost -= np.sum(selected['now_cost'])
        return selected


# Segregates players into 3 types - Most efficient, most costliest, underdogs
def cost_analysis(players, cost, number, player_type=None):
    players_selected = []
    efficient_player_count = int(number / 2)
    top_player_count = 1
    mid_player_count = number - efficient_player_count - top_player_count

    if player_type == "Defender":
        top_player_count = 3
        efficient_player_count = 2
        mid_player_count = 0

    # Midfielders make the most points hence all 5 top players are selected  within the provided budget
    if player_type == "Midfielder":
        top_player_count = 5
        mid_player_count = 0
        efficient_player_count = 0

    # Selects the top players within the provided  budget
    for index, row in players.iterrows():
        if top_player_count == 0:
            break
        if row['Fpl_ID'] not in players_selected and cost > row['now_cost']:
            players_selected.append(row['Fpl_ID'])
            players.loc[index, ['status']] = 1
            top_player_count -= 1
            cost = cost - row['now_cost']

    # Selects the mid range players (underdogs) within the provided  budget
    players = players.sort_values(
        by='now_cost', ascending=True).reset_index().drop(["index"], axis=1)
    for index, row in players.iterrows():
        if mid_player_count == 0:
            break
        if row['Fpl_ID'] not in players_selected and cost > row['now_cost']:
            players_selected.append(row['Fpl_ID'])
            players.loc[index, ['status']] = 1
            mid_player_count -= 1
            cost = cost - row['now_cost']

    # Selects the most efficient players within the provided budget
    players = players.sort_values(by='efficiency', ascending=False).reset_index().drop(["index"], axis=1)
    for index, row in players.iterrows():
        if efficient_player_count == 0:
            break
        if row['Fpl_ID'] not in players_selected and cost > row['now_cost']:
            players_selected.append(row['Fpl_ID'])
            players.loc[index, ['status']] = 1
            efficient_player_count -= 1
            cost = cost - row['now_cost']

    players = players.sort_values(by='aggregate', ascending=False).reset_index().drop(["index"], axis=1)
    # returns selected players to cost_wrapper
    return players[players['status'] == 1]


# Z-score computer
def compute_score(player_z, metrics):
    for item in metrics[1:-3]:
        player_z['soccer_one_' + item] = (player_z[item] - np.mean(player_z[item])) / np.std(player_z[item])
    return player_z
