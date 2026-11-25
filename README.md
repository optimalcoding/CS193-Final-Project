# Formula 1 Race Results Scraper

A command-line Python tool designed to scrape F1 starting grid and race result grids for any F1 race from the OpenF1 API and export an organized dataset to CSV files.

## The Problem
Find a quick and convenient way to pull clean, organized F1 race session data without needing to navigate other platforms. The aim of the project is to provide an easy-to-use, typo-resistant terminal tool that can save the bare-bones starting grid and race results locally.

## How It Works

1) User is asked for the year they would like to view
2) User is then prompted for a country from the provided list for that year
3) If a country has multiple circuits (USA or Italy for example), the user will then be prompted to choose which circuit they would like to view
4) The program accesses the OpenF1 API and packages the starting grid and race results (including driver names, team names, acronyms, and total tire stints) into two CSV files stored on the user's local machine

## System Diagram
![System Diagram](docs/f1.drawio.png)

## Tech Stack
- **Languages:** Python 3
- **API:** OpenF1
- **Data Manipulation:** Pandas, Difflib, Urllib.request, JSON
- **Storage:** .CSV Files on client local machine

## Instructions

1) Clone the repository and navigate into project folder:

        git clone https://github.com/optimalcoding/F1-Data-Scraper.git
        cd F1-Data-Scraper

2) Create and activate a virtual environment:

        For Windows Powershell do:

        python3 -m venv .venv
        .venv\Scripts\Activate.ps1

        MacOS and Linux can do:

        python3 -m venv .venv
        source .venv/bin/activate

3) Install Dependencies:

        pip install -r requirements.txt

4) Run the script:

        python src/main.py

## Example Usage & Output

        Welcome to the F1 Data Fetcher! Follow the prompts to fetch data for a specific year and country.

        Enter the year: 2024
        ['Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'China', 'United States', 'Italy', 'Monaco', 'Canada', 'Spain', 'Austria', 'United Kingdom', 'Hungary', 'Belgium', 'Netherlands', 'Azerbaijan', 'Singapore', 'Mexico', 'Brazil', 'Qatar', 'United Arab Emirates']
        Enter the country name (e.g. Netherlands, United Kingdom): United States
        Multiple circuits found for the given country and year. Please select one:
           session_key   location
        0         9506      Miami
        1         9616     Austin
        2         9635  Las Vegas
        Enter the row digit of the desired circuit: 1
        Saved starting_grid.csv
        Saved race_results.csv

## Project Roadmap
- [x] **MVP:** Query OpenF1 `/sessions`, `/starting_grid`, and `/session_result` endpoints and export to `starting_grid.csv` and `race_results.csv`
- [x] **Driver & Team Mapping (`feature/driver-names`):** Fetch driver rosters from `/drivers` and map car numbers to full names, team names, and acronyms
- [x] **Multi-Circuit Selection (`feature/multi-circuit`):** Prompt user to choose a circuit when a country hosts multiple Grands Prix in one year
- [x] **Dynamic Country Validation (`feature/country-matching`):** Fetch valid host countries dynamically per season and auto-correct spelling mistakes using `difflib`
- [x] **Function Refactoring (`feature/function`):** Extract driver dictionary creation into `get_driver_dict(session_key)`
- [x] **Tire Stint Tracking (`feature/weather`):** Query `/stints` to calculate and map each driver's `total_stints` into `race_results.csv`
- [ ] **Future Enhancement:** Integrate session weather averages (`/weather`) and full season championship standings

## Demo Video
[Watch the Project Demo Video Here](INSERT_YOUR_VIDEO_LINK_HERE)
