import matplotlib as plt
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import models.PlayerOverall as po
import plotly.express as px
import os
import pandas as pd
import plotly.graph_objects as go


def radar_charts_player_stats(*argv):
    categories = ['Ball_Skills', 'Defence', 'Physical', 'Shooting', 'Mental', 'Passing', 'Goalkeeper']
    categories = [*categories, categories[0]]
    if len(argv) == 1:
        player_df = po.overall_id(argv[0])
        print(player_df)
        player = player_df.iloc[0, 1:8]
        player = [*player, player[0]]
        # print(player)
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
# radar_charts_player_stats(231677)

# Scatter PLot from season player stats
def subplot_scatter(graphs, fwds, mids, defenders, goalies, xaxis, yaxis, y):
    if graphs == 4:
        title = ""
        title = y.replace("_", " ")
        title = title.capitalize() + " vs Cost"
        fig = make_subplots(rows=int(graphs / 2), cols=2, specs=[[{"type":"scatter"}, {"type":"scatter"}],
                                                                 [{"type":"scatter"}, {"type":"scatter"}]],
                            subplot_titles=("Forwards", "Midfields", "Defenders", "Goalkeepers"))

        fig.add_trace(get_fig_scatter(fwds, y), row=1, col=1)
        fig.add_trace(get_fig_scatter(mids, y), row=1, col=2)
        fig.add_trace(get_fig_scatter(defenders, y), row=2, col=1)
        fig.add_trace(get_fig_scatter(goalies, y), row=2, col=2)

        fig.update_traces(
            mode='markers',
            marker={'sizemode': 'area',
                    'sizeref': 0.01})
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(title_text=xaxis, row=i, col=j)
                fig.update_yaxes(title_text=yaxis, row=i, col=j)

        fig.update_layout(title_text=title + " Forwards / Midfields / Defenders / Goalkeepers")


        fig.show()
    else:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(get_fig_scatter(df, xaxis, yaxis, title, y))
        fig.update_xaxes(title_text=xaxis, row=1, col=1)
        fig.update_yaxes(title_text=yaxis, row=1, col=1)


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
        "Points per game: %{y:,}<br>" +
        "Cost: %{x:,}" +
        "<extra></extra>",
        marker_size=df[y + '_int'],
    )
    return trace


def get_fig_trace():
    print('getting trace')


# Testing scatter plot

# def scatter_plot_for_player_points(plot_type = )


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
