import os, requests, logging
from dotenv import load_dotenv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class NbaBettingLine:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)

    def get_game_lines(self) -> dict[str, float]:
        nbakey = "basketball_nba"
        url = f"https://odds.p.rapidapi.com/v4/sports/{nbakey}/odds?regions=us&oddsFormat=decimal&markets=spreads&dateFormat=iso"
        headers = {
            'X-RapidAPI-Key': os.getenv('NEXT_PUBLIC_RAPIDAPI_KEY'),
            'X-RapidAPI-Host': os.getenv('NEXT_PUBLIC_RAPIDAPI_ODDS_HOST')
        }

        result = None
        try:
            response = requests.get(url, headers=headers)
            result = response.json()
        except Exception as e:
            logger.error(f'Script Continued: Odds Failed to load: {e}')
            result = []

        points = {}
        for game in result:
            for bookmaker in game['bookmakers']:
                if bookmaker['key'] == 'fanduel':
                    for market in bookmaker['markets']:
                        if market['key'] == 'spreads':
                            for outcome in market['outcomes']:
                                points[outcome["name"]] = float(outcome['point'])
        print(f'{len(points)} NBA Game Odds loaded')
        return points
