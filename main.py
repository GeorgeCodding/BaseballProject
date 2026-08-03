#!/usr/bin/env python3
import requests
import time
import csv
import json
from pathlib import Path

def fetch_and_save_json(url, save_path):
    # Fetch the data from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the JSON data
        data = response.json()

        file_path = Path(save_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the JSON data to a file
        with open(save_path, 'w') as file:
            json.dump(data, file, indent=4)
            
        print(f"Successfully saved JSON to {save_path}")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

def get_season_schedule(season_year):
    # Step 1: Hit the schedule endpoint to get all games for the {season_year} season
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season_year}"
    print("Fetching ", season_year," Schedule...")
    fetch_and_save_json(schedule_url, f"jsons/schedules/mlb_schedule_{season_year}.json")

def download_season_boxscores(schedule_file_path, output_dir="jsons/boxscores"):
    """
    Parses a schedule JSON file and fetches boxscores for all completed 
    regular season games.
    """
    with open(schedule_file_path, 'r') as f:
        schedule_data = json.load(f)

    for date_info in schedule_data.get('dates', []):
        for game in date_info.get('games', []):
            
            # Filter out Spring Training ('S') and Exhibition ('E') games
            if game.get('gameType') in ['S', 'E']:
                continue

            # Only process games that are finished
            if game.get('status', {}).get('abstractGameState') != 'Final':
                continue

            game_pk = game['gamePk']
            home_team = game['teams']['home']['team']['name']
            save_path = Path(output_dir) / home_team / f"boxscore_{game_pk}.json"

            # Skip network request if already downloaded
            if save_path.exists():
                continue

            boxscore_url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
            fetch_and_save_json(boxscore_url, save_path)
            
            time.sleep(0.1)

# Run the function and print the first 5 games to verify it works
if __name__ == "__main__":
    for i in range(2025, 2026):
        get_season_schedule(i)
        season_json_path = f"jsons/schedules/mlb_schedule_{i}.json"
        boxscore_save_path = f"jsons/boxscores/{i}/"
        download_season_boxscores(season_json_path, boxscore_save_path)
