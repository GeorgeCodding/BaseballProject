import json
import csv

def extract_game_features_to_csv(json_filepath, csv_filepath, desired_features):
    """
    Extracts specific features from an MLB boxscore JSON and writes a flattened row to CSV.
    
    :param json_filepath: Path to the input JSON file (e.g., 'boxscore_631534.json')
    :param csv_filepath: Path to the output CSV file
    :param desired_features: List of string names for stats to pull (e.g., ['runs', 'hits', 'era'])
    """
    #Load the raw JSON data
    try:
        with open(json_filepath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {json_filepath}")
        return

    # Navigate to the teamStats level in the MLB API structure
    try:
        away_stats = data['teams']['away']['teamStats']
        home_stats = data['teams']['home']['teamStats']
    except KeyError as e:
        print(f"Error: JSON structure doesn't match expected MLB API format. Missing {e}")
        return

    #A dictionary to hold our single row of game data
    game_row = {}
    game_row['game_id'] = json_filepath.split('_')[-1].replace('.json', '') # Optional: Extract ID from filename

    # Helper function to dig out features and prefix them so columns don't overlap
    def parse_team_stats(team_data, team_prefix):
        categories = ['batting', 'pitching', 'fielding']
        
        for category in categories:
            if category in team_data:
                for feature in desired_features:
                    # If the requested stat exists in this category, extract it
                    if feature in team_data[category]:
                        # Create a clean ML column name (e.g., 'home_pitching_strikeOuts')
                        column_name = f"{team_prefix}_{category}_{feature}"
                        game_row[column_name] = team_data[category][feature]

    # Extract for both away and home teams
    parse_team_stats(away_stats, 'away')
    parse_team_stats(home_stats, 'home')

    # Write the flattened dictionary to a CSV
    with open(csv_filepath, 'w', newline='') as csvfile:
        # fieldnames dictates the column headers
        writer = csv.DictWriter(csvfile, fieldnames=game_row.keys())
        
        writer.writeheader()
        writer.writerow(game_row)
        
    print(f"Success! {len(game_row)} columns extracted and saved to {csv_filepath}")

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Define the exact metrics you want your neural network to learn from
    features_to_pull = [ 
        'hits', 
        'homeRuns', 
        'strikeOuts', 
        'baseOnBalls', 
        'leftOnBase', 
        'whip'
    ]

    # Run the function on your uploaded file
    extract_game_features_to_csv(
        json_filepath='boxscore_631534.json',
        csv_filepath='game_631534_model_input.csv',
        desired_features=features_to_pull
    )