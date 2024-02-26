import pandas as pd
import requests as req
from datetime import date, timedelta
import json

latitude = None
longitude = None
start_date = None
end_date = None

location_file = open('location') 
for lines in location_file.readlines():
    if lines.startswith('latitude'):
        latitude = float(lines.strip().split('=')[1])
    if lines.startswith('longitude'):
        longitude = float(lines.strip().split('=')[1])  
location_file.close()


date_range_file = open('timekeeper') 
for lines in date_range_file.readlines():
    if lines.startswith('start_date'):
        start_date = date.fromisoformat(lines.strip().split('=')[1])
        end_date = start_date
date_range_file.close()

api_url = "https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,rain,pressure_msl&daily=temperature_2m_max,temperature_2m_min".format(latitude = latitude, longitude = longitude, start_date = start_date, end_date = end_date)

response = req.get(api_url)

json_response = json.loads(response.content)

new_dataset_hourly = pd.DataFrame.from_dict(json_response['hourly'])
new_dataset_daily = pd.DataFrame.from_dict(json_response['daily'])

old_dataset_hourly = pd.read_csv('dataset/Mumbai-hourly.csv')
old_dataset_daily = pd.read_csv('dataset/Mumbai-daily.csv')

final_dataset_hourly = pd.concat([old_dataset_hourly, new_dataset_hourly], ignore_index=True)
final_dataset_daily = pd.concat([old_dataset_daily, new_dataset_daily], ignore_index=True)
final_dataset_hourly.to_csv('dataset/Mumbai-hourly.csv')
final_dataset_daily.to_csv("dataset/Mumbai-daily.csv")

start_date = start_date + timedelta(days=1)
date_file = open('timekeeper', 'w')
date_file.write('start_date={start_date}'.format(start_date=start_date))
date_file.close()