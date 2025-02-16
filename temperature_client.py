import requests
import time

base_url = 'http://homepi5:8080/temp-humidity'
latest_url = '/latest'
history_url = '/history'
location_paramter = 'location=bedroom-2'

timeframes = {
    "HOUR": 60*60,
    "DAY": 60*60*24,
    "MONTH": 60*60*24*30
}

def fetch_temperature_data():
    data = fetch_temp_humidity_data()
    current_temp = data.get('temperature')
    return current_temp

def fetch_humidity_data():
    data = fetch_temp_humidity_data()
    current_humidity = data.get('humidity')
    return current_humidity

def fetch_temp_humidity_data():
    response = requests.get(base_url + latest_url + '?' + location_paramter)
    return response.json()

def fetch_historical_data(timeframe): #Needs timeframe option
    current_time_seconds = int(time.time())
    start_time_seconds = current_time_seconds - timeframes[timeframe]
    response = requests.get(base_url + history_url + "?" + location_paramter + f"&startTime={start_time_seconds}&endTime={current_time_seconds}")
    return response.json()