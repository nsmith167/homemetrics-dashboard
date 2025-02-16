from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import weather_client
import time

temp_toast = dbc.Toast(
    [html.H2(id="weather-temp-display", className="me-2")],
    header="Temperature",
)
humidity_toast = dbc.Toast(
    [html.H2(id="weather-humidity-display", className="me-2")],
    header="Humidity",
)

readings_row = dbc.Stack([temp_toast, humidity_toast], direction="horizontal", gap=3)

timeframe_options = {"Past Hour": "HOUR", "Past 24 Hours": "DAY", "Past Month": "MONTH"}
timeframe_keys = list(timeframe_options.keys())

weather_tab_content = dbc.Card(
    dbc.CardBody(
        [
            readings_row,
            dcc.Dropdown(timeframe_keys, timeframe_keys[0], id='weather-timeframe-selection', style={'margin-top': '10px', 'margin-bottom': '10px'}),
            dcc.Graph(id='weather-temp-graph'),
            dcc.Graph(id='weather-humidity-graph')
        ]
    ),
    className="mt-3",
)

@callback(
    Output("weather-temp-display", "children"), [Input("refresh-button", "n_clicks")]
)
def on_button_click_temperature_update(n):
    return str(round(float(weather_client.fetch_temperature_data()),2)) + u'\N{DEGREE SIGN}'
    
@callback(
    Output("weather-humidity-display", "children"), [Input("refresh-button", "n_clicks")]
)
def on_button_click_humidity_update(n):
    return str(round(float(weather_client.fetch_humidity_data()),2)) + '%'

@callback(
    Output('weather-temp-graph', 'figure'),
    Input('weather-timeframe-selection', 'value')
)
def update_temperature_graph(value):
    df = get_historical_temp_humidity_data(value)
    return px.line(df, x='timestamp', y='temperature')

@callback(
    Output('weather-humidity-graph', 'figure'),
    Input('weather-timeframe-selection', 'value')
)
def update_humidity_graph(value):
    df = get_historical_temp_humidity_data(value)
    return px.line(df, x='timestamp', y='humidity')

def get_historical_temp_humidity_data(timeframe):
    temp_data = weather_client.fetch_historical_data(timeframe_options[timeframe])
    df = pd.DataFrame(temp_data)
    df["timestamp"] = df["timestamp"].map(lambda timestamp: convert_epoch_seconds_to_local_time(timestamp))
    df["temperature"] = df["temperature"].map(lambda temp: celsius_to_fahrenheit(temp))
    return df

def convert_epoch_seconds_to_local_time(seconds):
    local_time_struct = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time_struct)

def celsius_to_fahrenheit(degrees_celsius):
    return (degrees_celsius * 9/5) + 32 

def weather_content():
    return weather_tab_content