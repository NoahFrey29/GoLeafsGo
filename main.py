import json
from pathlib import Path
from data_ingestion import main as fetch_data
from data_processing import PlayerDataProcessor
from database import app, PlayerList 

def main():
    print("Starting NHL Player Data Pipeline")
    print("=" * 50)
    
    # Ingest data from data_ingestion.py
    print("\n[1/3] Fetching raw player data...")
    if not fetch_data():
        print("Failed to fetch data from API")
        return False
    
    # Process data from data_processing.py
    print("\n[2/3] Processing data...")
    processor = PlayerDataProcessor(Path("data/nhl_players.json"))
    try:
        processor.load_data()
        processed_data = processor.process_players()
        processor.save_processed_data(Path("data/processed_players.json"), processed_data)
        print(f"Processed {len(processed_data)} players")
    except Exception as e:
        print(f"Processing failed: {e}")
        return False
    
    # Store the data using the API Database integration from database.py
    print("\n[3/3] Loading to database...")
    with app.app_context():
        try:
            with open("data/processed_players.json", 'r') as f:
                players_data = json.load(f)

            print(players_data)

            player_list = PlayerList()
            response = player_list.post(players_data=players_data)
            
            print(f"Database insertion result: {response[0]['message']}")
            if response[0].get('errors'):
                print("\nErrors encountered:")
                for error in response[0]['errors']:
                    print(f"- {error}")
            
            return response[1] == 201
            
        except Exception as e:
            print(f"Database loading failed: {e}")
            return False

if __name__ == "__main__":
    if not main():
        print("\nPipeline failed at some step")