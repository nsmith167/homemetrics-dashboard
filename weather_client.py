import requests
import time

base_url = 'http://homepi5:8080/weather/local'
latest_url = '/latest'
history_url = '/history'
zip_code_parameter = 'zipCode=19460'

timeframes = {
    "HOUR": 60*60,
    "DAY": 60*60*24,
    "MONTH": 60*60*24*30
}

def fetch_temperature_data():
    data = fetch_temp_humidity_data()
    current_temp = data.get('temperature')
    return celsius_to_fahrenheit(current_temp)

def fetch_humidity_data():
    data = fetch_temp_humidity_data()
    current_humidity = data.get('humidity')
    return current_humidity

def fetch_temp_humidity_data():
    response = requests.get(base_url + latest_url + '?' + zip_code_parameter)
    return response.json()

def fetch_historical_data(timeframe):
    current_time_seconds = int(time.time())
    start_time_seconds = current_time_seconds - timeframes[timeframe]
    response = requests.get(base_url + history_url + "?" + zip_code_parameter + f"&startTime={start_time_seconds}&endTime={current_time_seconds}")
    return response.json()

def celsius_to_fahrenheit(degrees_celsius):
    return (degrees_celsius * 9/5) + 32 