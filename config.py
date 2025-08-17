from dotenv import load_dotenv
import os

load_dotenv()  

def get_api_key() -> str:
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        raise ConfigError("RAPIDAPI_KEY not found in environment variables or .env file")
    return api_key

API_CONFIG = {
    'host': "sports-information.p.rapidapi.com",
    'base_path': "/nhl",
    'key': get_api_key()
}

TEAMS = {
    'maple_leafs': 21
}