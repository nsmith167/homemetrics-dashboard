from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import temperature_client
import time

temp_toast = dbc.Toast(
    [html.H2(id="temperature-display", className="me-2")],
    header="Temperature",
)
humidity_toast = dbc.Toast(
    [html.H2(id="humidity-display", className="me-2")],
    header="Humidity",
)

readings_row = dbc.Stack([temp_toast, humidity_toast], direction="horizontal", gap=3)

timeframe_options = {"Past Hour": "HOUR", "Past 24 Hours": "DAY", "Past Month": "MONTH"}
timeframe_keys = list(timeframe_options.keys())

def temperature_content():
    return dbc.Card(
        dbc.CardBody(
            [
                readings_row,
                dcc.Dropdown(timeframe_keys, timeframe_keys[0], id='dropdown-selection', style={'margin-top': '10px', 'margin-bottom': '10px'}),
                dcc.Graph(id='temperature-graph'),
                dcc.Graph(id='humidity-graph')
            ]
        ),
        className="mt-3",
    )   

@callback(
    Output("temperature-display", "children"), [Input("refresh-button", "n_clicks")]
)
def on_button_click_temperature_update(n):
    return str(round(float(temperature_client.fetch_temperature_data()),2)) + u'\N{DEGREE SIGN}'
    
@callback(
    Output("humidity-display", "children"), [Input("refresh-button", "n_clicks")]
)
def on_button_click_humidity_update(n):
    return str(round(float(temperature_client.fetch_humidity_data()),2)) + '%'

@callback(
    Output('temperature-graph', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_temperature_graph(value):
    df = get_historical_temp_humidity_data(value)
    return px.line(df, x='timestamp', y='temperature')

@callback(
    Output('humidity-graph', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_humidity_graph(value):
    df = get_historical_temp_humidity_data(value)
    return px.line(df, x='timestamp', y='humidity')

def get_historical_temp_humidity_data(timeframe):
    temp_data = temperature_client.fetch_historical_data(timeframe_options[timeframe])
    df = pd.DataFrame(temp_data)
    df["timestamp"] = df["timestamp"].map(lambda timestamp: convert_epoch_seconds_to_local_time(timestamp))
    return df

def convert_epoch_seconds_to_local_time(seconds):
    local_time_struct = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time_struct)