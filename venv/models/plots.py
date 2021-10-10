import matplotlib as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import PlayerOverall as po

def radar_charts_player_stats(*argv):
    categories = ['Ball_Skills', 'Defence', 'Physical', 'Shooting', 'Mental','Passing','Goalkeeper']
    categories = [*categories, categories[0]]
    if len(argv)== 1:
        player_df = po.overall_id(argv[0])
        print(player_df)
        player = player_df.iloc[0,1:8]
        player = [*player, player[0]]
        print(player)
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
radar_charts_player_stats(231677,189509)


# import plotly.graph_objects as go
# animals=['giraffes', 'orangutans', 'monkeys']
#
# fig = go.Figure(data=[
#     go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
#     go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
# ])
# # Change the bar mode
# fig.update_layout(barmode='stack')
# fig.show()
#
# import plotly.express as px
#
# df = px.data.iris()
# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
#                  size='petal_length', hover_data=['petal_width'])
# fig.show()