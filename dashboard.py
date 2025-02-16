from dash import Dash, html
import dash_bootstrap_components as dbc
import logging
import temperature_dashboard
import weather_dashboard

logging.basicConfig(level=logging.INFO)


app = Dash(external_stylesheets=[dbc.themes.MINTY])



refresh_button = html.Div(
    dbc.Button("Refresh", id="refresh-button", className="me-2"),
    style={'margin-top': '50px', 'margin-bottom': '25px'}
)


tabs = dbc.Tabs(
    [
        dbc.Tab(temperature_dashboard.temperature_content(), label="Nursey Temperature"),
        dbc.Tab(weather_dashboard.weather_content(), label="Local Weather")
    ]
)

app.layout = dbc.Container([
    html.H1(children='Temperature & Humidity Dashboard', style={'margin-top': '10px', 'margin-bottom': '10px'}),
    tabs,
    refresh_button
])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=False)