from main_func import get_stats
import dash
from dash import dcc
from dash import html
import plotly.express as px
from setup import setup_df
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__)

play_df, play_list, form_df, men_df, rushed_df, down_con_df = setup_df()

play_fig = px.bar(play_df, x='Down', y='Percentage', color='Play Type', barmode='group', height=400, range_y=[0, 100],
                  title='Play Type Percentage', text='Percentage', color_discrete_sequence=['#03202F', '#A71930', 'DimGrey', 'DarkGrey'])
play_fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

form_fig = px.bar(form_df, x='Formation', y='Percentage', color='Play Type', barmode='group', height=400,
                  range_y=[0, 100],
                  title='Play Type by Formation Percentage', text='Percentage', color_discrete_sequence=['#03202F', '#A71930',])
form_fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

men_fig = px.bar(men_df, x='Men in Box', y='Avg Yards', color='Play Type', barmode='group', height=400, range_y=[0, 40],
                 title='Avg Yards per Men in Box', text='Avg Yards', color_discrete_sequence=['#03202F', '#A71930',])
men_fig.update_traces(texttemplate='%{text:.2f}', textposition='inside')

rushed_fig = px.bar(rushed_df, x='Players Rushed', y='Avg Yards', color='Legend', barmode='group', height=400,
                    range_y=[0, 30],
                    title='Avg Passing Yards per Players Rushed', text='Avg Yards', color_discrete_sequence=['#03202F'])
rushed_fig.update_traces(texttemplate='%{text:.2f}', textposition='inside')

down_con_fig = px.bar(down_con_df, x='Down', y='Conversion %', color='Legend', barmode='group', height=400,
                    range_y=[0, 100],
                    title='1st Down Conversion % per Down', text='Conversion %', color_discrete_sequence=['#03202F'])
down_con_fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

downs = ['1st Down', '2nd Down', '3rd Down', '4th Down']


app.layout = html.Div(
    children=[
        html.H1("2020 Houston Texans Offense", style={'color': '#03202F', 'fontSize': 50, 'textAlign': 'center'}),
        html.P(
            children="Analyze key statistics of the 2020 Houston Texans Offense"
            ,style={'color': '#A71930', 'fontSize': 25, 'textAlign': 'center'}
        ),
        dcc.Graph(figure=play_fig),
        dcc.Dropdown(
            id="dropdown-noredzone",
            options=[{"label": x, "value": x} for x in downs],
            value=downs[0],
            clearable=False,
        ),
        dcc.Graph(id='bar-chart-noredzone'),
        dcc.Dropdown(
            id="dropdown-redzone",
            options=[{"label": x, "value": x} for x in downs],
            value=downs[0],
            clearable=False,
        ),
        dcc.Graph(id='bar-chart-redzone'),
        dcc.Dropdown(
            id="dropdown-goalline",
            options=[{"label": x, "value": x} for x in downs],
            value=downs[0],
            clearable=False,
        ),
        dcc.Graph(id='bar-chart-goalline'),
        dcc.Graph(figure=form_fig),
        dcc.Graph(figure=men_fig),
        dcc.Graph(figure=rushed_fig),
        dcc.Graph(figure=down_con_fig)

    ]
)


@app.callback(
    Output("bar-chart-noredzone", "figure"),
    Output("bar-chart-redzone", "figure"),
    Output("bar-chart-goalline", "figure"),
    Input("dropdown-noredzone", "value"),
    Input("dropdown-redzone", "value"),
    Input("dropdown-goalline", "value"))
def update_bar_chart(noredzone, redzone, goalline):
    index1 = downs.index(noredzone)
    index2 = downs.index(redzone)
    index3 = downs.index(goalline)
    title1 = f'Non Redzone {noredzone} Play Percentage'
    title2 = f'Redzone {redzone} Play Percentage'
    title3 = f'Goalline {goalline} Play Percentage'
    fig1 = px.bar(play_list[0][index1], x='Down', y='Percentage', color='Play Type', barmode='group', height=400,
                  range_y=[0, 100], title=title1, text='Percentage', color_discrete_sequence=['#03202F', '#A71930', 'DimGrey', 'DarkGrey'])
    fig1.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

    fig2 = px.bar(play_list[1][index2], x='Down', y='Percentage', color='Play Type', barmode='group', height=400,
                  range_y=[0, 100], title=title2, text='Percentage', color_discrete_sequence=['#03202F', '#A71930', 'DimGrey', 'DarkGrey'])
    fig2.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

    fig3 = px.bar(play_list[2][index3], x='Down', y='Percentage', color='Play Type', barmode='group', height=400,
                  range_y=[0, 100], title=title3, text='Percentage', color_discrete_sequence=['#03202F', '#A71930', 'DimGrey', 'DarkGrey'])
    fig3.update_traces(texttemplate='%{text:.2f}%', textposition='inside')

    return fig1, fig2, fig3


if __name__ == "__main__":
    app.run_server(debug=True)
