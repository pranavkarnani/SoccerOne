import matplotlib as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import PlayerOverall as po
import plotly.express as px
import os
import pandas as pd
import plotly.graph_objects as go

def radar_charts_player_stats(*argv):
    categories = ['Ball_Skills', 'Defence', 'Physical', 'Shooting', 'Mental','Passing','Goalkeeper']
    categories = [*categories, categories[0]]
    if len(argv)== 1:
        player_df = po.overall_id(argv[0])
        print(player_df)
        player = player_df.iloc[0,1:8]
        player = [*player, player[0]]
        #print(player)
        fig = go.Figure(
            data=[
                go.Scatterpolar(r=player, theta=categories, fill='toself', name=player_df.Name.to_string()),
            ],
            layout=go.Layout(
                title=go.layout.Title(text='Player Stats'),
                polar={'radialaxis': {'visible': True}},
                showlegend=True
            )
        )
        pyo.plot(fig)
    elif len(argv) == 2:
        player_df_1 = po.overall_id(argv[0])
        player_df_2 = po.overall_id(argv[1])
        player_1 = player_df_1.iloc[0, 1:8]
        player_1 = [*player_1, player_1[0]]
        player_2 = player_df_2.iloc[0, 1:8]
        player_2 = [*player_2, player_2[0]]
        print(player_1)
        print(player_2)
        fig = go.Figure(
            data=[
                go.Scatterpolar(r=player_1, theta=categories, fill='toself', name=player_df_1.Name.to_string()),
                go.Scatterpolar(r=player_2, theta=categories, fill='toself', name=player_df_2.Name.to_string()),
            ],
            layout=go.Layout(
                title=go.layout.Title(text='Player Comparison'),
                polar={'radialaxis': {'visible': True}},
                showlegend=True
            )
        )
        pyo.plot(fig)


# Testing radar charts
#radar_charts_player_stats(231677)

# Scatter PLot from season player stats
def scatter_plot_for_player_points(*argv):
    os.chdir('../data/')
    df = pd.read_csv("season_player_stats_df.csv")
    df = df[:25]
    print(df['points_per_game'])
    fig = px.scatter(df, x="now_cost", y="points_per_game",
                     size="now_cost", hover_data=['fullname']) #what should the size be dependent on
    fig.show()


#Testing scatter plot

#def scatter_plot_for_player_points(plot_type = )



# Send over a df and then we build the chart from the points column
# X will be points column and y will just be a column wiht one value
# color will be based on player name
def expected_points():
    df = px.data.tips()
    df['team'] = 'Team1'
    fig = px.bar(df, x="total_bill", y="team", color='day', orientation='h',
                 height=400,
                 title='Expected Points from the team')
    fig.show()
expected_points()



