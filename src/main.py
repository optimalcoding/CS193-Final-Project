from urllib.request import urlopen
import json
from difflib import get_close_matches
import pandas as pd


def get_driver_dict(session_key):
    response = urlopen(f'https://api.openf1.org/v1/drivers?session_key={session_key}')
    data = json.loads(response.read().decode('utf-8'))
    data_df = pd.DataFrame(data)[['driver_number', 'first_name', 'last_name', 'name_acronym', 'team_name']]

    name_dict = {}
    team_dict = {}
    acronym_dict = {}
    for i in range(len(data_df)):
        driver_number = data_df['driver_number'][i]
        first_name = data_df['first_name'][i]
        last_name = data_df['last_name'][i]
        name_acronym = data_df['name_acronym'][i]
        team_name = data_df['team_name'][i]

        name_dict[driver_number] = f"{first_name} {last_name}"
        team_dict[driver_number] = team_name
        acronym_dict[driver_number] = name_acronym

    return name_dict, team_dict, acronym_dict

print("Welcome to the F1 Data Fetcher! Follow the prompts to fetch data for a specific year and country.")
print()
year = input("Enter the year: ").strip()
response = urlopen(f'https://api.openf1.org/v1/sessions?session_name=Qualifying&year={year}')
all_sessions = json.loads(response.read().decode('utf-8'))
places_df = pd.DataFrame(all_sessions)[['country_name', 'location']]
country_list = list(places_df['country_name'].unique())
print(country_list)
raw_country = input("Enter the country name (e.g. Netherlands, United Kingdom): ").strip().title()
if raw_country not in country_list:
    closest = get_close_matches(raw_country, country_list, n=1, cutoff=0.6)
    if len(closest) > 0:
        print(f"Did you mean '{closest[0]}'? Using '{closest[0]}'...")
        raw_country = closest[0]
    else:
        print(f"Error: '{raw_country}' is not a valid F1 host country for {year}.")
        exit()
country = raw_country.replace(" ", "%20")

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Qualifying&year={year}')
data = json.loads(response.read().decode('utf-8'))
if len(data) > 1:
    print("Multiple circuits found for the given country and year. Please select one:")
    df = pd.DataFrame(data)[['session_key', 'location']]
    print(df)
    choice = int(input("Enter the row digit of the desired circuit: ").strip())
    quali_key = data[choice]['session_key']
    circuit_name = data[choice]['location']
else:
    quali_key = data[0]['session_key']
    circuit_name = data[0]['location']

name_dict, team_dict, acronym_dict = get_driver_dict(quali_key)

response = urlopen(f'https://api.openf1.org/v1/starting_grid?session_key={quali_key}')
data = json.loads(response.read().decode('utf-8'))
startgrid_df = pd.DataFrame(data)[['position', 'driver_number']]
startgrid_df['driver_name'] = startgrid_df['driver_number'].map(name_dict)
startgrid_df['team_name'] = startgrid_df['driver_number'].map(team_dict)
startgrid_df['name_acronym'] = startgrid_df['driver_number'].map(acronym_dict)
startgrid_df.to_csv('starting_grid.csv', index=False)
print("Saved starting_grid.csv")

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Race&year={year}')
data = json.loads(response.read().decode('utf-8'))
df = pd.DataFrame(data)[['session_key', 'location']]
race_key = df[df['location'] == circuit_name]['session_key'].iloc[0]

name_dict, team_dict, acronym_dict = get_driver_dict(race_key)

response = urlopen(f'https://api.openf1.org/v1/session_result?session_key={race_key}')
data = json.loads(response.read().decode('utf-8'))
race_df = pd.DataFrame(data)[['position', 'driver_number', 'gap_to_leader']]
race_df['driver_name'] = race_df['driver_number'].map(name_dict)
race_df['team_name'] = race_df['driver_number'].map(team_dict)
race_df['name_acronym'] = race_df['driver_number'].map(acronym_dict)
race_df.to_csv('race_results.csv', index=False)
print("Saved race_results.csv")
