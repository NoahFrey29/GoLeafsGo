import json
from typing import List, Dict
from pathlib import Path

class PlayerDataProcessor:
    
    def __init__(self, input_file: Path):
        self.input_file = input_file
        self.players = []
        
    def load_data(self) -> None:
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not data or 'team' not in data or 'athletes' not in data['team']:
                raise ValueError("Invalid data structure - missing team or athletes")
                
            self.players = data['team']['athletes']
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")

    def process_players(self) -> List[Dict]:
        processed_players = []
        
        for player in self.players:
            try:
                processed = {
                    'full_name': player.get('fullName'),
                    'age': player.get('age'),
                    'height': self._convert_height(player.get('height')),
                    'weight': player.get('weight'),
                    'position': player.get('position', {}).get('displayName'),
                    'jersey_number': player.get('jersey')
                }
                processed_players.append(processed)
            except Exception as e:
                print(f"Skipping player due to processing error: {e}")
                
        return processed_players
    
    def _convert_height(self, inches: int) -> str:
        if not inches:
            return "N/A"
        feet = inches // 12
        remaining_inches = inches % 12
        return f"{feet}' {remaining_inches}\""
    
    def save_processed_data(self, output_file: Path, data: List[Dict]) -> None:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Successfully saved processed data to {output_file}")
        except Exception as e:
            print(f"Error saving processed data: {e}")

if __name__ == "__main__":
    input_path = Path("data/nhl_players.json")
    output_path = Path("data/processed_players.json")
    
    processor = PlayerDataProcessor(input_path)
    try:
        processor.load_data()
        processed_data = processor.process_players()
        processor.save_processed_data(output_path, processed_data)
        
        print("\nSample processed player:")
        print(json.dumps(processed_data[0], indent=2))
        
    except Exception as e:
        print(f"Processing failed: {e}")