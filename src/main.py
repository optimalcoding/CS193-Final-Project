from urllib.request import urlopen
import json
import pandas as pd

#country = input("Enter the country name (e.g. Netherlands, Great Britain): ").strip().title().replace(" ", "%20")
#session_type = input("Enter the session type (e.g., Qualifying, Sprint Qualifying): ").strip().title().replace(" ", "%20")
#year = input("Enter the year: ")

response = urlopen('https://api.openf1.org/v1/sessions?country_name=Belgium&session_name=Race&year=2023')
data = json.loads(response.read().decode('utf-8'))
print(data)

#if session_type == "Race":
#    print(session_type)     
    #session_type = "Race"
    #response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name={session_type}&year={year}')
    #data = json.loads(response.read().decode('utf-8'))
    #session_key = data[0]['session_key']
    #print (f"Session Key: {session_key}")
    #response = urlopen(f'https://api.openf1.org/v1/starting_grid?session_key={session_key}')
    #data = json.loads(response.read().decode('utf-8'))
    #df = pd.DataFrame(data)
    #print(df[['position', 'driver_number', 'lap_duration']])
    #response = urlopen(f'https://api.openf1.org/v1/session_result?session_key={session_key}')
    #data = json.loads(response.read().decode('utf-8'))
    #df = pd.DataFrame(data)
    #print(df[['position', 'driver_number', 'lap_duration']])

