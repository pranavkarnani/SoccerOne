# Importing the required libraries
import requests
from urllib.request import urlopen
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import os

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'

# Fixture Difficulty - Compute the fixture difficult rating for each game for team.
def fixture_difficulty():
    # Downloading the fixtures from online source and saving it as a csv
    fixtures_url = 'https://cdn.bettingexpert.com/assets/England-Premier-League-fixture-2021-2022.csv'
    req = requests.get(fixtures_url)
    url_content = req.content
    csv_file = open(DATA_PATH+'England-Premier-League-fixture-2021-2022.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()

    # Adding gameday column to each column (10 i's selected as each gameday has 10 games)
    gameday_nested = [(i,i,i,i,i,i,i,i,i,i) for i in range(1,39)]
    gameday = [item for sublist in gameday_nested for item in sublist]


    # Creating dataframe df from csv file
    df = pd.read_csv(DATA_PATH+'England-Premier-League-fixture-2021-2022.csv', sep=',',index_col=False)

    # Deleting columns not required
    del df['League']

    # Creating the gameday column
    df['Gameday'] = gameday

    # Rearranging the columns
    df = df[['Gameday', 'Date', 'Home', 'Away']]

    # Setting the index
    df.index = np.arange(1, len(df)+1)

    # Creating dataframe team_data_df from teams.csv file
    team_data_df = pd.read_csv(DATA_PATH+'teams.csv', sep=',',index_col=1)

    # Deleting columns not required
    team_data_df.drop(['Unnamed: 0', 'short_name', 'strength', 'strength_attack_home',
                      'strength_attack_away', 'strength_defence_home', 'strength_defence_away'],
                      axis=1, inplace = True)

    # Converting home_strength and away_strength columns in team_data_df to dict to be used for mapping
    home_strength = dict(zip(team_data_df.Club, team_data_df.strength_overall_home))
    away_strength = dict(zip(team_data_df.Club, team_data_df.strength_overall_away))


    # Creating dataframes home_df and away_df
    home_df = df['Home'].to_frame()
    away_df = df['Away'].to_frame()

    # Adding home_strength and away_strength values to the respective home and away teams
    df['Home_Strength'] = df['Home'].map(home_strength)
    df['Away_Strength'] = df['Away'].map(away_strength)

    # Predicting winning chance for each fixture using MinMaxScaler
    df['Home_Win'] = 100*((df['Home_Strength']-np.min(df['Home_Strength']))/
                           (np.max(df['Home_Strength'])-np.min(df['Home_Strength'])))

    df['Away_Win'] = 100*((df['Away_Strength']-np.min(df['Away_Strength']))/
                           (np.max(df['Away_Strength'])-np.min(df['Away_Strength'])))

    # Predicting win percent against the opposite team
    # and adding it to the 'Pred_Winning_Team' column
    df['Home_Win_Percent'] = 100*((df['Home_Win'])/((df['Home_Win'])+df['Away_Win']))
    df['Away_Win_Percent'] = 100*((df['Away_Win'])/((df['Home_Win'])+df['Away_Win']))
    df['Pred_Winning_Team'] = np.where(df['Home_Win'] > df['Away_Win'], df['Home'], df['Away'])

    # Function to getLosingTeam
    def getLosingTeam(Home, Away, Pred_Winning_Team):
        if Home == Pred_Winning_Team:
            return Away
        else:
            return Home

    # Adding the 'Pred_Losing_Team' column
    df['Pred_Losing_Team']= df.apply(lambda row: getLosingTeam(row.Home, row.Away, row.Pred_Winning_Team), axis=1)

    # Adding the 'Win_Percent' column for the predicted winning team
    df['Win_Percent'] = np.where(df['Home_Win'] > df['Away_Win'], df['Home_Win_Percent'], df['Away_Win_Percent'])
    df['Win_Percent'] = df['Win_Percent'].round(2)

    # Deleting columns not required
    df.drop(['Home_Win', 'Away_Win','Home_Strength', 'Away_Strength', 'Home_Win_Percent',
             'Away_Win_Percent'],axis=1, inplace=True)


    # Bucketing 'Win_Percent' as 'Win Rating'
    def getBucket(winPercent):
        if winPercent>=90:
            return 0
        if winPercent>=60:
            return 1
        if winPercent>=50:
            return 2

    # Adding the bucket values to the 'Win Rating' for the 'Pred_Winning_Team'
    df['Win_Rating']= df.apply(lambda row: getBucket(row.Win_Percent), axis=1)
    # Adding the buckets values to the 'Loss Rating' for the 'Pred_Losing_Team'
    df['Loss_Rating']=5-df['Win_Rating']


    # Converting the 'Date' from object to datetime object
    df['Date']=pd.to_datetime(df['Date'])

    # Function to determine the next gameday using today
    # and to stop after the next four gamedays post that
    def get5GameDays(df):
        from_next_gameday_df = df.loc[(df['Date'] > dt.datetime.today())]
        gamedayMin = from_next_gameday_df['Gameday'].min()
        gamedayMax = from_next_gameday_df['Gameday'].min()+4

        # adding the filtered data to the selected_gamedays_df and returning that to next_5_gamedays_df
        selected_gamedays_df = from_next_gameday_df[from_next_gameday_df['Gameday']<=gamedayMax]

        return selected_gamedays_df


    next_5_gamedays_df=get5GameDays(df)


    # Building the dataframe for the heatmap
    # Converting the team names to a list
    teams_list = team_data_df['Club'].tolist()
    # Converting the unique gamedays to a list
    gameday_list = next_5_gamedays_df['Gameday'].unique().tolist()

    # heatmap_df with index as teams_list and columns as gameday_list
    heatmap_df = pd.DataFrame(index = teams_list, columns = gameday_list)


    # Function to populate heatmap_df cells based on winning/losing team and gameday
    def assignHeatMapBuckets(gameday, home, away, winTeam, loseTeam, winVal, lossVal):

        heatmap_df.loc[winTeam][gameday]=winVal
        heatmap_df.loc[loseTeam][gameday]=lossVal

    # for loop to iterate through all the cells of next_5_gamedays_df and adding them to the heatmap_df
    # these values will determine the color in the heatmap based on their values
    for row in next_5_gamedays_df.iterrows():
        assignHeatMapBuckets(row[1][0],row[1][2],row[1][3], row[1][4],row[1][5],row[1][7],row[1][8] )



    # Creating dataframe labels_df to annotate the heatmap
    labels_df= pd.DataFrame(index = teams_list, columns = gameday_list)

    # Function to populate heatmap_df labels based on home/away team and gameday
    def assignLabel(gameday, home, away, winTeam, loseTeam, winVal, lossVal):
        labels_df.loc[home][gameday]= away + ' (A)'
        labels_df.loc[away][gameday]= home + ' (H)'

    # for loop to iterate through all the cells of next_5_gamedays_df and adding annotations to the heatmap_df
    # these values will be displayed on the heatmap
    for row in next_5_gamedays_df.iterrows():
        assignLabel(row[1][0],row[1][2],row[1][3], row[1][4],row[1][5],row[1][7],row[1][8] )

    # Converting df to array to use in the sns heatmap
    labels_Array=labels_df.to_numpy()


    # Plotting the heatmap
    sns.set(rc = {'figure.figsize':(40,10)})
    sns.set(font_scale = 0.8)
    plot = sns.heatmap(heatmap_df.astype(float), annot=labels_Array,cmap ='RdYlGn_r', fmt = '', vmin=0, vmax=5,
                       linewidths=0.5,linecolor='white', cbar_kws={'label': 'Fixture Difficulty Rating'})
    plot.set_xlabel('Gameday', fontsize = 15)
    plot.set_ylabel('Team', fontsize = 15)
    plot.set_xticklabels(plot.get_xticklabels(), size = 10)
    plot.set_yticklabels(plot.get_yticklabels(), size=10)
    plot.set_title('Fixture Difficulty', fontsize = 18)
    bottom, top = plot.get_ylim()
    plt.savefig(DATA_PATH+'Teams_Fixture_Difficulty.pdf')
    plt.show()

fixture_difficulty()