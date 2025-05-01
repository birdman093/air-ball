import os, requests, logging
from dotenv import load_dotenv

logger = logging.getLogger('NbaBettingLineApi')

class NbaBettingLineApi:
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

        try:
            response = requests.get(url, headers=headers)
            result = response.json()
        except Exception as e:
            logger.error(f'** NON-BREAKING ** Failed to load Api: {e}')
            result = []

        points = {}
        for game in result:
            for bookmaker in game['bookmakers']:
                if bookmaker['key'] == 'fanduel':
                    for market in bookmaker['markets']:
                        if market['key'] == 'spreads':
                            for outcome in market['outcomes']:
                                points[outcome["name"]] = float(outcome['point'])
        logger.info(f'Loaded {len(points)} games')
        logger.info(", ".join(f"{game}: {point}" for game, point in points.items()))
        return points
    
    def valid_game_lines(self, home_line: float, away_line:float) -> bool:
        return abs(abs(home_line) - abs(away_line)) < 0.1
