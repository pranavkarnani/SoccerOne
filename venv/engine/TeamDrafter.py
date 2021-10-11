import os
import re

import numpy as np
import pandas as pd
import datetime
import knapsack01

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


def make_team():
    soccerOne = pd.read_csv(DATA_PATH + 'soccerOneMaster.csv', index_col=0)
    fwds = analyze(soccerOne[soccerOne['position'] == 'Forward'], 'Forward')
    mids = analyze(soccerOne[soccerOne['position'] == 'Midfielder'], 'Midfielder')
    defs = analyze(soccerOne[soccerOne['position'] == 'Defender'], 'Defender')
    goalies = analyze(soccerOne[soccerOne['position'] == 'Goalkeeper'], 'Goalkeeper')
    topPlayers = fwds.append([mids, defs, goalies], ignore_index=True)
    # cost_analysis(topPlayers.loc[:, ['Name', 'position', 'Club', 'Fpl_ID', 'Fifa_ID', 'aggregate', 'now_cost']])


def analyze(players, player_type):
    fpl = pd.read_csv(DATA_PATH + 'season_player_stats_df.csv', index_col=0)
    player_attr = fpl.copy()
    metrics = []

    if player_type == "Forward":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'minutes', 'threat',
                   'ict_index', 'goals_scored', 'assists', 'form', 'value_season', 'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]

    elif player_type == "Midfielder":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'minutes', 'threat',
                   'ict_index', 'influence', 'creativity', 'assists', 'form', 'value_season', 'news', 'news_added',
                   'now_cost']
        player_attr = fpl.loc[:, metrics]

    elif player_type == "Defender":
        metrics = ['id', 'ep_this', 'points_per_game', 'chance_of_playing_this_round', 'minutes',
                   'ict_index', 'clean_sheets', 'assists', 'form', 'value_season', 'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]

    elif player_type == "Goalkeeper":
        metrics = ['id', 'ep_this', 'points_per_game', 'selected_by_percent', 'chance_of_playing_this_round',
                   'clean_sheets', 'saves', 'form', 'value_season', 'news', 'news_added', 'now_cost']
        player_attr = fpl.loc[:, metrics]

    selection_metrics = players.loc[:, ['Name', 'position', 'Club', 'Fpl_ID', 'Fifa_ID']].merge(player_attr,
                                                                                     how="left", left_on='Fpl_ID',
                                                                                     right_on='id')

    selection_metrics = selection_metrics[selection_metrics['chance_of_playing_this_round'] != 0]
    selection_metrics['now_cost'] = selection_metrics['now_cost'] / 10
    normalized_players = compute_score(selection_metrics, metrics)
    normalized_players['aggregate'] = normalized_players.loc[:,
                                      [col for col in normalized_players.columns if 'soccer_one_' in col]].sum(axis=1)
    normalized_players['aggregate'] = normalized_players['aggregate']/len(metrics)
    normalized_players = normalized_players[normalized_players['aggregate'] > 0]
    normalized_players = normalized_players.sort_values(by=['aggregate', 'now_cost'], ascending=False)
    player_list = (len(normalized_players)) if (len(normalized_players) <= 20) else 20

    #Display image
    cost = 100
    normalized_players["status"] = 0
    normalized_players = normalized_players.sort_values(
        by='now_cost', ascending=False).reset_index().drop(["index"], axis=1)

    if player_type == "Forward":
        x = best_weight(normalized_players, 'now_cost', 21, 0, 0)
        cost -= np.sum(x[x['status'] == 1]['now_cost'])
        print(x[x["status"] == 1])
    if player_type == "Goalkeeper":
        x = best_weight(normalized_players, 'now_cost', 9, 0, 0)
        cost -= np.sum(x[x['status'] == 1]['now_cost'])
        print(x[x["status"] == 1])
    elif player_type == "Defender":
        x = best_weight(normalized_players, 'now_cost', 28, 0, 0)
        cost -= np.sum(x[x['status'] == 1]['now_cost'])
        print(x[x["status"] == 1])
    elif player_type == "Midfielder":
        x = best_weight(normalized_players, 'now_cost', 42, 0, 0)
        cost -= np.sum(x[x['status'] == 1]['now_cost'])
        print(x[x["status"] == 1])

    print(cost)
# cost_analysis(normalized_players, , len(normalized_players))

    return normalized_players[0:player_list]


def compute_score(player_z, metrics):
    for item in metrics[1:-3]:
        player_z['soccer_one_'+item] = (player_z[item] - np.mean(player_z[item]))/np.std(player_z[item])
    return player_z


def best_weight(data, reason, rest, values, index):
    if rest < np.min(data.loc[range(index, len(data)), reason]) or (index == len(data)):
        return values
    else:
        if rest >= data[reason][index]:
            data.loc[index, 'status'] = 1
            rest = rest - data[reason][index]
            values = values + data["aggregate"][index]
            index = index + 1
            values = best_weight(data, reason, rest, values, index)
            return data
        else:
            index = index + 1
            values = best_weight(data, reason, rest, values, index)
            return data

make_team()
