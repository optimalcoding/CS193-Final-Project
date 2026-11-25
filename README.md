Formula 1 Race Results Scraper

A command-line Python tool designed to scrape F1 starting grid and race result grids for any F1 race from the OpenF1 API and exports an organized dataset to CSV files.

The Problem:
Find a quick and convenient way to pull clean, organized F1 race session data without needing to navigate other platforms. The aim of the project is to provide an easy-to-use, typo-resistant terminal tool that can save the bare-bones starting grid and race results locally.

How it works:

1) User is asked for the year they would like to view
2) User is then prompted for a country from the provided dropdown for that year
3) If a country has multiple circuits (USA or Italy for example), the user will then be prompted to choose which circuit they would like to view
4) The program accesses OpenF1 API and packages the starting grid and race results into two CSV files stored on the user's local machine

System Diagram:
![System Diagram](docs/f1.drawio.png)

Tech Stack
- Languages: Python 3
- API: fastf1
- Data Manipulation: Pandas
- Storage: .CSV Files on client local machine

Instructions:

Clone the repo by using git clone https://github.com/optimalcoding/F1-Data-Scraper.git
And then go into the directory with: cd F1-Data-Scraper

For Windows Powershell do:
python3 -m venv .venv
.venv\Scripts\Activate.ps1

MacOS and Linux can do:
python3 -m venv .venv
source .venv/bin/activate

Install Dependencies:
pip install -r requirements.txt

Run the script:
python src/main.py

