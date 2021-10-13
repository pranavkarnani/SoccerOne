# File: plots.py
# Names: Jaison Jose, Neha Joshi, Pranav Karnani, Preet Jain
# Imports - Generates player overall csv - data_processors.PlayerOverall.py

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import data_processors.PlayerOverall as po
import plotly.express as px
import os
import pandas as pd
import plotly.graph_objects as go

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'

# Function to build radar charts for the different player stats that we have scraped
def radar_charts_player_stats(*argv):
    categories = ['Ball_Skills', 'Defence', 'Physical', 'Shooting', 'Mental', 'Passing', 'Goalkeeper']
    categories = [*categories, categories[0]]
    if len(argv) == 1:
        player_df = po.overall_id(argv[0].Fifa_ID)
        player = player_df.iloc[0, 1:8]
        player = [*player, player[0]]
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
    elif len(argv) > 1:
        player_df_1 = po.overall_id(argv[0].Fifa_ID)
        player_df_2 = po.overall_id(argv[1].Fifa_ID)
        player_1 = player_df_1.iloc[0, 1:8]
        player_1 = [*player_1, player_1[0]]
        player_2 = player_df_2.iloc[0, 1:8]
        player_2 = [*player_2, player_2[0]]

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


# Scatter PLot from season player stats
def subplot_scatter(graphs, fwds, mids, defenders, goalies, xaxis, yaxis, y,marker_size_ref):
    if graphs == 4:
        title = ""
        title = y.replace("_", " ")
        title = title.capitalize() + " vs Cost"
        fig = make_subplots(rows=int(graphs / 2), cols=2, specs=[[{"type":"scatter"}, {"type":"scatter"}],
                                                                 [{"type":"scatter"}, {"type":"scatter"}]],
                            subplot_titles=("Forwards", "Midfielders", "Defenders", "Goalkeepers"))

        fig.add_trace(get_fig_scatter(fwds, y), row=1, col=1)
        fig.add_trace(get_fig_scatter(mids, y), row=1, col=2)
        fig.add_trace(get_fig_scatter(defenders, y), row=2, col=1)
        fig.add_trace(get_fig_scatter(goalies, y), row=2, col=2)

        fig.update_traces(
            mode='markers',
            marker={'sizemode': 'area',
                    'sizeref': marker_size_ref})
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(title_text=xaxis, row=i, col=j)
                fig.update_yaxes(title_text=yaxis, row=i, col=j)

        fig.update_layout(title_text=title + " By Position")


        fig.show()
    else:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(get_fig_scatter(df, xaxis, yaxis, title, y))
        fig.update_xaxes(title_text=xaxis, row=1, col=1)
        fig.update_yaxes(title_text=yaxis, row=1, col=1)


# Get the traces for individual scatter plots that are populated in the subplot_scatter
def get_fig_scatter(df, y):
    df[y + '_int'] = df[y].astype(int)
    trace = go.Scatter(
        x=df['now_cost'],
        y=df[y],
        hovertext=df['Name'],
        text=df['ep_this'],
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "Expected points: %{text:,}<br>" +
         y.replace('_',' ').capitalize()+" : %{y:,}<br>" +
        "Cost: %{x:,}" +
        "<extra></extra>",
        marker_size=df[y + '_int'],
    )
    return trace

def recommended_players_encircle(graphs, fwds, mids, defenders, goalies, xaxis, yaxis,
                                 y,marker_size_ref,selected_fwd,selected_mid,selected_def,
                                 selected_goalies):
    if graphs == 4:
        title = ""
        title = y.replace("_", " ")
        title = title.capitalize() + " vs Cost"
        fig = make_subplots(rows=int(graphs / 2), cols=2, specs=[[{"type":"scatter"}, {"type":"scatter"}],
                                                                 [{"type":"scatter"}, {"type":"scatter"}]],
                            subplot_titles=("Forwards", "Midfielders", "Defenders", "Goalkeepers"))

        fig.add_trace(get_fig_scatter(fwds, y), row=1, col=1)
        fig.add_trace(get_fig_scatter(mids, y), row=1, col=2)
        fig.add_trace(get_fig_scatter(defenders, y), row=2, col=1)
        fig.add_trace(get_fig_scatter(goalies, y), row=2, col=2)

        selected_fwd_fifa_id = selected_fwd['Fifa_ID']
        selected_mid_fifa_id = selected_mid['Fifa_ID']
        selected_def_fifa_id = selected_def['Fifa_ID']
        selected_goalie_fifa_id = selected_goalies['Fifa_ID']
        selected_fwd_points = pd.DataFrame()
        selected_mid_points = pd.DataFrame()
        selected_def_points = pd.DataFrame()
        selected_goalie_points = pd.DataFrame()
        #print(fwds[['Fifa_ID','ep_this','now_cost']])

        for i in selected_fwd_fifa_id:
            selected_fwd_points = selected_fwd_points.append(fwds.loc[fwds['Fifa_ID'] == i])
        for i in selected_mid_fifa_id:
            selected_mid_points = selected_mid_points.append(mids.loc[mids['Fifa_ID'] == i])
        for i in selected_def_fifa_id:
            selected_def_points = selected_def_points.append(defenders.loc[defenders['Fifa_ID'] == i])
        for i in selected_goalie_fifa_id:
            selected_goalie_points = selected_goalie_points.append(goalies.loc[goalies['Fifa_ID'] == i])

        # print(selected_fwd_points[['Name','Fifa_ID','ep_this','now_cost']])
        # print(selected_mid_points[['Name','Fifa_ID','ep_this','now_cost']])
        # print(selected_def_points[['Name','Fifa_ID','ep_this','now_cost']])
        # print(selected_goalie_points[['Name','Fifa_ID','ep_this','now_cost']])
        #
        # print(selected_fwd_points['now_cost'].min())
        # print(selected_fwd_points['now_cost'].max())
        fig.add_shape(type="circle",
                      xref="paper", yref="paper",
                      x0=selected_fwd_points['now_cost'].min(), y0=selected_fwd_points['ep_this'].min(),
                      x1=selected_fwd_points['now_cost'].max(), y1=selected_fwd_points['ep_this'].max(),
                      opacity=0.4,
                      line_color="#00008b",
                      fillcolor="#ADD8E6",
                      row=1,
                      col=1
                      )
        fig.add_shape(type="circle",
                      xref="paper", yref="paper",
                      x0=selected_mid_points['now_cost'].min(), y0=selected_mid_points['ep_this'].min(),
                      x1=selected_mid_points['now_cost'].max(), y1=selected_mid_points['ep_this'].max(),
                      opacity=0.1,
                      line_color="#8B0000",
                      fillcolor="#FF7F7F",
                      row=1,
                      col=2
                      )
        fig.add_shape(type="circle",
                      xref="paper", yref="paper",
                      x0=selected_def_points['now_cost'].min(), y0=selected_def_points['ep_this'].min(),
                      x1=selected_def_points['now_cost'].max(), y1=selected_def_points['ep_this'].max(),
                      opacity=0.1,
                      line_color="#030B07",
                      fillcolor="#90EE90",
                      row=2,
                      col=1
                      )
        fig.add_shape(type="circle",
                      xref="x", yref="y",
                      x0=selected_goalie_points['now_cost'].min(), y0=selected_goalie_points['ep_this'].min(),
                      x1=selected_goalie_points['now_cost'].max(), y1=selected_goalie_points['ep_this'].max(),
                      opacity=0.1,
                      line_color="#290916",
                      fillcolor="#CBC3E3",
                      row=2,
                      col=2
                      )
        fig.update_traces(
            mode='markers',
            marker={'sizemode': 'area',
                    'sizeref': marker_size_ref})
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(title_text=xaxis, row=i, col=j)
                fig.update_yaxes(title_text=yaxis, row=i, col=j)

        fig.update_layout(title_text=title + " By Position")


        fig.show()
    else:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(get_fig_scatter(df, xaxis, yaxis, title, y))
        fig.update_xaxes(title_text=xaxis, row=1, col=1)
        fig.update_yaxes(title_text=yaxis, row=1, col=1)

# Send over a df and then we build the chart from the points column
# X will be points column and y will just be a column with one value
# color will be based on player name
def expected_points(df):
    fig = px.bar(df, x="ep_this", y="Team", color='Name',
                 color_discrete_sequence=['#00876c','#3d9a70','#64ad73','#89bf77','#afd17c','#d6e184','#fff18f','#fdd576','#fbb862','#f59b56','#ee7d4f','#e35e4e','#d43d51','#923737','#652b2b'],
                 orientation='h',
                 height=400,
                 title='Expected Points from the team',
                 )

    fig.show()

#Dot chart to build the number of times a player has been mentioned in the news
def player_news_plots():
    player_news = pd.read_csv(DATA_PATH+"featured.csv")
    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    ax.hlines(y=player_news.Player, xmin=1, xmax=5, color='gray', alpha=0.7, linewidth=1, linestyles='dashdot')
    ax.scatter(y=player_news.Player, x=player_news.Times, s=75, color='orange', alpha=0.7)

    # Title, Label, Ticks and Ylim
    ax.set_title('No. of times players are mentioned in the news', fontdict={'size': 22})
    ax.set_xlabel('News mentions')
    ax.set_yticks(player_news.Player)
    ax.set_yticklabels(player_news.Player, fontdict={'horizontalalignment': 'right'})
    ax.set_xlim(0, 6)
    plt.show()

# Build a subplot with all the pie charts that have been built based on player metrics and score
def pie_subplot(metric_1,score_1,metric_2,score_2,title,subplot1_title,subplot2_title):
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],
                        subplot_titles=(subplot1_title, subplot2_title))
    fig.add_trace(position_analytics_pie(metric_1, score_1), row=1, col=1)
    fig.add_trace(position_analytics_pie(metric_2, score_2), row=1, col=2)


    fig.update_layout(title_text=title)
    fig.show()

# Return the individual traces for the subplot function above using metrics and score.
def position_analytics_pie(metrics,score):
   trace = go.Pie(
        values=score[1:],
        labels=metrics[1:]
        )
   return trace



