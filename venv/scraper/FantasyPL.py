import pandas as pd
import requests

def getFantasyPL():
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = response.json()
    events_json = data['events']
    teams_json = data['teams']
    season_player_stats_json = data['elements']

    team_data_columns = ["id", "code","name", "short_name", "strength", "strength_overall_home", "strength_overall_away",
                         "strength_attack_home", "strength_attack_away", "strength_defence_home",
                         "strength_defence_away"]
    event_data_columns = ["id", "name", "deadline_time", "finished"]
    season_player_stats_columns = ["chance_of_playing_next_round", "chance_of_playing_this_round", "code", "ep_next",
                                   "ep_this", "event_points", "first_name", "form", "id", "news", "news_added",
                                   "now_cost",
                                   "points_per_game", "second_name", "selected_by_percent", "team_code", "total_points",
                                   "value_form", "value_season", "web_name", "minutes", "goals_scored", "assists",
                                   "clean_sheets", "goals_conceded", "own_goals", "penalties_saved", "penalties_missed",
                                   "yellow_cards", "red_cards", "saves", "bonus", "influence", "creativity", "threat",
                                   "ict_index", "influence_rank_type", "creativity_rank_type", "threat_rank_type",
                                   "ict_index_rank", "ict_index_rank_type", "penalties_order", "penalties_text"]

    events = []
    for json_object in events_json:
        item = []
        for column in event_data_columns:
            item.append(json_object[column])
        events.append(item)
    events_df = pd.DataFrame(events, columns=event_data_columns)
    events_df.to_csv('events.csv')

    teams = []
    for json_object in teams_json:
        item = []
        for column in team_data_columns:
            item.append(json_object[column])
        teams.append(item)
    teams_df = pd.DataFrame(teams, columns=team_data_columns)
    teams_df.to_csv('teams.csv')

    season_player_stats = []
    for json_object in season_player_stats_json:
        item = []
        for column in season_player_stats_columns:
            item.append(json_object[column])
        season_player_stats.append(item)
    season_player_stats_df = pd.DataFrame(season_player_stats, columns=season_player_stats_columns)
    season_player_stats_df.to_csv('season_player_stats_df.csv')
