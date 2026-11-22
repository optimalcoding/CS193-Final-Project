from urllib.request import urlopen
import json
import pandas as pd

country = input("Enter the country name (e.g. Netherlands, United Kingdom): ").strip().title().replace(" ", "%20")
#session_type = input("Enter the session type (e.g., Qualifying, Sprint Qualifying): ").strip().title().replace(" ", "%20")
year = input("Enter the year: ")

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Qualifying&year={year}')
data = json.loads(response.read().decode('utf-8'))
key = data[0]['session_key']

response = urlopen(f'https://api.openf1.org/v1/starting_grid?session_key={key}')
data = json.loads(response.read().decode('utf-8'))
df = pd.DataFrame(data)
print(df[['position', 'driver_number']])

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Race&year={year}')
data = json.loads(response.read().decode('utf-8'))
key = data[0]['session_key']

response = urlopen(f'https://api.openf1.org/v1/session_result?session_key={key}')
data = json.loads(response.read().decode('utf-8'))
df = pd.DataFrame(data)
print(df[['position', 'driver_number', 'gap_to_leader']])