from data_processors.SoccerOneMaster import makeMaster
from data_processors.FifaCleaner import cleanFifa
from engine.TeamDrafter import make_team, cost_wrapper
import os
import pandas as pd
import models.plots as plots
import engine.fixture_difficulty as fd

makeMaster()

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
DATA_PATH = FILE_PATH + '/data/'


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
            plots.radar_charts_player_stats(soccer_master_temp.loc[player_stat]['Fifa_ID'])
            print("Compare against another player(Y/N)?")
            player_stats_input = input()
            if (player_stats_input == 'Y'):
                print(soccer_master_temp.loc[:30, ['Name', 'position', 'Club', 'Fifa_ID', 'Overal']])
                player_stat_2 = input()
                player_stat_2 = int(player_stat_2)
                if (player_stat >= 0 and player_stat <= 30):
                    if (player_stat >= 0 and player_stat <= 30):
                        plots.radar_charts_player_stats(soccer_master_temp.loc[player_stat]['Fifa_ID'],
                                                        soccer_master_temp.loc[player_stat_2]['Fifa_ID'])
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
            3. Back to main menu""")
            plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Points per Game", 'points_per_game',.01)
            player_pick_selection = input()
            if (player_pick_selection == "1"):
                print("Advanced Analytics")
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Form", 'form',0.01)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Value this season", 'value_season',0.01)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Total Points", 'total_points',0.1)
                plots.subplot_scatter(4, fwds, mids, defs, goalies, "Cost", "Influence Creativity Threat Index", 'ict_index',0.1)
                break
            elif (player_pick_selection == "2"):
                selected_fwd = cost_wrapper(fwds,"Forward")
                selected_mid = cost_wrapper(mids,"Midfielder")
                selected_defender = cost_wrapper(defs,"Defender")
                selected_goalkeeper = cost_wrapper(goalies,"Goalkeeper")

                final_recommendation = pd.concat([selected_fwd.loc[:,['Name','position','ep_this']],selected_mid.loc[:,['Name','position','ep_this']]])
                final_recommendation = pd.concat([final_recommendation.loc[:,['Name','position','ep_this']],selected_defender.loc[:,['Name','position','ep_this']]])
                final_recommendation = pd.concat([final_recommendation.loc[:,['Name','position','ep_this']],selected_goalkeeper.loc[:,['Name','position','ep_this']]])
                final_recommendation['Team'] = 'Recommended Picks'
                print("Our Recommendation")
                print(final_recommendation)
                plots.expected_points(final_recommendation)
                break
            elif (player_pick_selection == "3"):
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
        print("League Standings")
    elif (first_selection == "5"):
        break
    else:
        print('Incorrect input')
        pass
