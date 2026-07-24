#!/usr/bin/env python3
import requests
import time
import csv

def get_nationals_2026_batting_logs():
    team_id = 120 # MLB's official ID for the Nationals
    season = 2026

    # Step 1: Hit the schedule endpoint to get all games for the 2026 season
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={team_id}&season={season}"
    print("Fetching 2026 Schedule...")

    schedule_response = requests.get(schedule_url)
    schedule_data = schedule_response.json() # Parse the JSON response

    batting_logs = []

    print("Fetching boxscore for each game...")
    for date_info in schedule_data.get('dates', []):
        for game in date_info.get('games', []):
            game_pk = game['gamePk'] # The unique Game ID
            game_date = game['officialDate']
            status = game['status']['statusCode']
            
            # Only pull boxscores for games that are Final ('F'), Game Over ('O'), or Completed Early ('I')
            if status not in ['F', 'O', 'I']:
                continue 
                
            # Request the specific boxscore for this Game ID
            boxscore_url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
            box_res = requests.get(boxscore_url)
            box_data = box_res.json()
            
            teams = box_data.get('teams', {})
            
            # Determine if the Nationals were the home or away team to grab the right stats
            if teams.get('home', {}).get('team', {}).get('id') == team_id:
                nat_stats = teams['home']['teamStats']['batting']
                opponent = teams['away']['team']['name']
            else:
                nat_stats = teams['away']['teamStats']['batting']
                opponent = teams['home']['team']['name']
                
            # Step 3: Extract the specific batting metrics you need
            # You can add more metrics here like OBP, SLG, etc.
            batting_logs.append({
                'Date': game_date,
                'Opponent': opponent,
                'At Bats': nat_stats.get('atBats', 0),
                'Runs': nat_stats.get('runs', 0),
                'Hits': nat_stats.get('hits', 0),
                'Home Runs': nat_stats.get('homeRuns', 0),
                'Strikeouts': nat_stats.get('strikeOuts', 0),
                'Walks': nat_stats.get('baseOnBalls', 0)
            })
            print(f"Pulled boxscore for {game_date} vs {opponent}.")
            # Sleep briefly to avoid overwhelming the MLB API servers
            time.sleep(0.1)

    return batting_logs

# Run the function and print the first 5 games to verify it works
if __name__ == "__main__":
    logs = get_nationals_2026_batting_logs()
    
    if logs: 
        filename = 'nationals_2026_batting_logs.csv'
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['Date', 'Opponent', 'At Bats', 'Runs', 'Hits', 'Home Runs', 'Strikeouts', 'Walks']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            for log in logs:
                writer.writerow(log)
        print(f"\nSuccess! Pulled {len(logs)} completed games and saved them to '{filename}'.")
    else:
        print("\nNo completed games were found to save.")