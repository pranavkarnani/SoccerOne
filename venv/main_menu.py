import numpy as np
from data_processors.SoccerOneMaster import makeMaster
from data_processors.FifaCleaner import cleanFifa
from engine.TeamDrafter import make_team, cost_wrapper
import os
import re
import datetime
import pandas as pd
import models.plots as plots
import engine.fixture_difficulty as fd

makeMaster()

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
DATA_PATH = FILE_PATH + '/data/'


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


def player_overall_stats(id):
    soccer_master = pd.read_csv(DATA_PATH + "soccerOneMaster.csv")
    player_overall = pd.read_csv(DATA_PATH + "player_overall.csv")
    soccer_master = soccer_master.loc[:, ['Name', 'position', 'Club', 'Fpl_ID', 'Fifa_ID']].merge(
        player_overall.loc[:, ['ID', 'Overal']],
        how="left",
        left_on='Fifa_ID',
        right_on='ID')
    if (id == 1):
        soccer_master_temp = soccer_master.loc[soccer_master['position'] == 'Forward']
    elif (id == 2):
        soccer_master_temp = soccer_master.loc[soccer_master['position'] == 'Midfielder']
    elif (id == 3):
        soccer_master_temp = soccer_master.loc[soccer_master['position'] == 'Defender']
    elif (id == 4):
        soccer_master_temp = soccer_master.loc[soccer_master['position'] == 'Goalkeeper']

    soccer_master_temp = soccer_master_temp.sort_values(
        by=['Overal'], ascending=False).reset_index().drop(["index"], axis=1)
    print(soccer_master_temp.loc[:30, ['Name', 'position', 'Club', 'Fifa_ID', 'Overal']])
    print("1. Enter the index against the player to see their stats")
    print("3. Press 2 to return to previous menu")
    player_stat = input()
    player_stat = int(player_stat)
    while (True):
        if (player_stat >= 0 and player_stat <= 30):
            plots.radar_charts_player_stats(soccer_master_temp.loc[player_stat, ['Fifa_ID']])
            print("Compare against another player(Y/N)?")
            player_stats_input = input()
            if (player_stats_input == 'Y'):
                print(soccer_master_temp.loc[:30, ['Name', 'position', 'Club', 'Fifa_ID', 'Overal']])
                print("Enter the index of the player to compare against")
                player_stat_2 = input()
                player_stat_2 = int(player_stat_2)
                if (player_stat_2 >= 0 and player_stat_2 <= 30):
                    plots.radar_charts_player_stats(soccer_master_temp.loc[player_stat,['Fifa_ID']],
                                                    soccer_master_temp.loc[player_stat_2,['Fifa_ID']])
                    break
            elif (player_stats_input == 'N'):
                break

        elif (player_stat == 2):
            break


while (True):
    print("""
   Analytics
1. Position 
2. Player 
3. Fixtures 
4. News
5. Exit""")
    first_selection = input()
    if (first_selection == "1"):
        fwds, mids, defs, goalies = make_team()
        while (True):
            print("""Here are the top players for each position
                       
            1. Advanced Analytics
            2. Our Recommendation (Top 15)
            3. Recommended Team Position Analytics
            4. Back to main menu""")
            plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Points per Game", 'points_per_game', 0.01)
            player_pick_selection = input()
            if (player_pick_selection == "1"):
                print("Advanced Analytics")
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Form", 'form', 0.01)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Value this season", 'value_season', 0.01)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Total Points", 'total_points', 0.1)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Influence Creativity Threat Index",
                                      'ict_index', 0.1)
                break

            elif (player_pick_selection == "2"):
                selected_fwd = cost_wrapper(fwds, "Forward")
                selected_mid = cost_wrapper(mids, "Midfielder")
                selected_defender = cost_wrapper(defs, "Defender")
                selected_goalkeeper = cost_wrapper(goalies, "Goalkeeper")

                final_recommendation = pd.concat([selected_fwd.loc[:, ['Name', 'position', 'ep_this']],
                                                  selected_mid.loc[:, ['Name', 'position', 'ep_this']]])
                final_recommendation = pd.concat([final_recommendation.loc[:, ['Name', 'position', 'ep_this']],
                                                  selected_defender.loc[:, ['Name', 'position', 'ep_this']]])
                final_recommendation = pd.concat([final_recommendation.loc[:, ['Name', 'position', 'ep_this']],
                                                  selected_goalkeeper.loc[:, ['Name', 'position', 'ep_this']]])
                final_recommendation['Team'] = 'Recommended Picks'
                print("Our Recommendations")
                print(final_recommendation)
                plots.expected_points(final_recommendation)

            elif (player_pick_selection == "3"):
                print("Position Analysis")
                fifa = pd.read_csv(DATA_PATH + get_file())
                selected_fwd = cost_wrapper(fwds, "Forward").loc[:, ['Name', 'Fifa_ID']]
                selected_mid = cost_wrapper(mids, "Midfielder").loc[:, ['Name', 'Fifa_ID']]
                selected_defender = cost_wrapper(defs, "Defender").loc[:, ['Name', 'Fifa_ID']]
                selected_goalkeeper = cost_wrapper(goalies, "Goalkeeper").loc[:, ['Name', 'Fifa_ID']]

                forward_metrics = ["ID", "Heading", "ShotPower", "Finishing", "LongShots", "Curve", "FKAcc", "Penalties",
                                   "Volleys", "Overal"]
                defender_metrics = ["ID", "Marking", "SlideTackle", "StandTackle", "Interceptions", "Stamina", "Overal"]
                mids_metrics = ["ID", "Crossing", "ShortPass", "LongPass", "Vision", "BallControl", "Agility", "Dribbling",
                                "Reactions", "Interceptions", "Overal"]
                goalkeeper_metrics = ["ID", "GKPositioning", "GKDiving", "GKHandling", "GKKicking", "GKReflexes", "Overal"]

                selected_fwd = selected_fwd.merge(fifa.loc[:, forward_metrics], how="left", left_on="Fifa_ID",
                                                  right_on="ID")
                print(selected_fwd)
                selected_mid = selected_mid.merge(fifa.loc[:, mids_metrics], how="left", left_on="Fifa_ID",
                                                  right_on="ID")
                selected_defender = selected_defender.merge(fifa.loc[:, defender_metrics], how="left",
                                                            left_on="Fifa_ID", right_on="ID")
                selected_goalkeeper = selected_goalkeeper.merge(fifa.loc[:, goalkeeper_metrics], how="left",
                                                                left_on="Fifa_ID", right_on="ID")
                forward_score = []
                midfield_score = []
                defender_score = []
                goalkeeper_score = []
                for item in forward_metrics[1:]:
                    print(item)
                    forward_score.append(np.mean(selected_fwd[item]))
                for item in defender_metrics[1:]:
                    print(item)
                    defender_score.append(np.mean(selected_defender[item]))
                for item in mids_metrics[1:]:
                    print(item)
                    midfield_score.append(np.mean(selected_mid[item]))
                for item in goalkeeper_metrics[1:]:
                    print(item)
                    goalkeeper_score.append(np.mean(selected_goalkeeper[item]))

                print(dict(zip(forward_metrics, forward_score)))
                print(dict(zip(mids_metrics, midfield_score)))
                print(dict(zip(defender_metrics, defender_score)))
                print(dict(zip(goalkeeper_metrics, goalkeeper_score)))

            elif (player_pick_selection == "4"):
                break

            else:
                print('Incorrect input')
                pass
    elif (first_selection == "2"):
        while (True):
            print("""
            2.1 Which position?
                1. Forward
                2. Midfield
                3. Defense
                4. Goalkeeper
                5. Back to main menu"""
                  )
            player_stat_position = input()
            if (player_stat_position == "1"):
                player_overall_stats(1)
            elif (player_stat_position == "2"):
                player_overall_stats(2)
            elif (player_stat_position == "3"):
                player_overall_stats(3)
            elif (player_stat_position == "4"):
                player_overall_stats(4)
            elif (player_stat_position == "5"):
                break
            else:
                print('Incorrect input')
                pass
    elif (first_selection == "3"):
        fd.fixture_difficulty()
    elif (first_selection == "4"):
        print( "Details of player mentions from News")
        plots.player_news_plots()
    elif (first_selection == "5"):
        break
    else:
        print('Incorrect input')
        pass
