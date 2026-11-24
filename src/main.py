from urllib.request import urlopen
import json
from difflib import get_close_matches
import pandas as pd

# OpenF1 API has a limitation where the full driver details aren't included in the base session results and just give the car number
# so I need to make a separate call to get the driver details and then map them to the car numbers in the session results
# I made this a function because I had two copies of these lines, one for the quali key and race key since sometimes the driver
# can be swapped in between sessions, so I need to make sure I get the correct driver details for each session
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
# For the next few lines I found a library in Python (difflib) that can estimate the closest match to a string and I implemented this after my
# own testing where sometimes I would misspell a country name and it failed immediately so I just take the user input for the year
# and parse it to the API and retrieve all of the participating countries for that year and then check if the user input is in that list
# Additionally I am already pulling sessions without country since the participating countries changes year to year and 
# doing so now can help me avoid hardcoding a list of countries and having to update it every year
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

# The %20 represents a space and there are some countries that are more than one word so after the country is found it gets processed
# to the way the API expects it to be formatted by removing the empty space
country = raw_country.replace(" ", "%20")

# Below here is where I make the API call to get the quali session for the input country and year and there is some logic to check
# for the countries that have multiple circuits in a year. Essentially when I took len(data) the OpenF1 API returns a list 
# where each list itself has an item in brackets and when there are multiple circuits for a country in a year the list
# will show multiple brackets
# I display the circuts that are available for the user to select and I map the inputs to the row number and pass that to later
# API calls

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
# This is a function call for the three dictionaries created in the function above to pull the driver name, driver team, and
# driver acronym that will be used to map the driver number in the starting grid and race results dataframes

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
# For this line since I saved the chosen circuit name from the quali session I can use the variable to find the corresponding
# race session key, call it from the API, and get the race results for that circuit and year without having to duplicate the logic 
# to find the circuit name again 
race_key = df[df['location'] == circuit_name]['session_key'].iloc[0]

name_dict, team_dict, acronym_dict = get_driver_dict(race_key)

response = urlopen(f'https://api.openf1.org/v1/session_result?session_key={race_key}')
data = json.loads(response.read().decode('utf-8'))
race_df = pd.DataFrame(data)[['position', 'driver_number', 'gap_to_leader']]
race_df['driver_name'] = race_df['driver_number'].map(name_dict)
race_df['team_name'] = race_df['driver_number'].map(team_dict)
race_df['name_acronym'] = race_df['driver_number'].map(acronym_dict)
response = urlopen(f'https://api.openf1.org/v1/stints?session_key={race_key}')
data = json.loads(response.read().decode('utf-8'))
tires_df = pd.DataFrame(data)[['driver_number', 'stint_number']]
stint_df = {}
for i in range(len(tires_df)):
    # OpenF1 API does not natively do the total stints as they record each stint as a separate row
    # so I have a for loop to iterate through the rows and create a dictionary where the key is the driver number and value is 
    # the total stints and I use .map to map the driver number in race result dataframe to the total stints one
    driver_number = tires_df['driver_number'][i]
    stint_number = tires_df['stint_number'][i]
    stint_df[driver_number] = stint_number
race_df['total_stints'] = race_df['driver_number'].map(stint_df)
race_df.to_csv('race_results.csv', index=False)
print("Saved race_results.csv")

