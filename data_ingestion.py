import http.client
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from config import API_CONFIG, TEAMS

API_HOST = API_CONFIG['host']
API_ENDPOINT = f"{API_CONFIG['base_path']}/team-players/{TEAMS['maple_leafs']}/"
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "nhl_players.json"

def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_players() -> Dict[str, Any]:
    conn = http.client.HTTPSConnection(API_HOST)
    try:
        conn.request("GET", API_ENDPOINT, headers={
            'x-rapidapi-host': API_HOST,
            'x-rapidapi-key': API_CONFIG['key']
        })
        
        res = conn.getresponse()
        
        if res.status != 200:
            raise Exception(f"API request failed with status {res.status}: {res.reason}")
        
        raw_data = res.read().decode('utf-8')
        return json.loads(raw_data)
        
    finally:
        conn.close()

def save_players(data: Dict[str, Any]) -> None:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
    print(f"Success! Player data saved to {OUTPUT_FILE}")

def main() -> bool:
    try:
        ensure_output_dir()
        print("Fetching player data...")
        player_data = fetch_players()
        
        if not player_data:
            print("Received empty response from API")
            return False
            
        save_players(player_data)
        return True
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response. The API might be returning invalid JSON. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

if __name__ == "__main__":
    if not main():
        print("Failed to complete player data fetch")