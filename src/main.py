from urllib.request import urlopen
import json
import pandas as pd

country = input("Enter the country name (e.g. Netherlands, United Kingdom): ").strip().title().replace(" ", "%20")
year = input("Enter the year: ").strip()

response = urlopen(f'https://api.openf1.org/v1/sessions?country_name={country}&session_name=Qualifying&year={year}')
data = json.loads(response.read().decode('utf-8'))
quali_key = data[0]['session_key']

response = urlopen(f'https://api.openf1.org/v1/drivers?session_key={quali_key}')
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
race_key = data[0]['session_key']

response = urlopen(f'https://api.openf1.org/v1/drivers?session_key={race_key}')
data = json.loads(response.read().decode('utf-8'))
#print(data)
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

response = urlopen(f'https://api.openf1.org/v1/session_result?session_key={race_key}')
data = json.loads(response.read().decode('utf-8'))
race_df = pd.DataFrame(data)[['position', 'driver_number', 'gap_to_leader']]
race_df['driver_name'] = race_df['driver_number'].map(name_dict)
race_df['team_name'] = race_df['driver_number'].map(team_dict)
race_df['name_acronym'] = race_df['driver_number'].map(acronym_dict)
race_df.to_csv('race_results.csv', index=False)
print("Saved race_results.csv")
