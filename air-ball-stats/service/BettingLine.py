import os, requests
from dotenv import load_dotenv

class NbaBettingLine:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, 'credentials', '.env.local')
        load_dotenv(env_path)

    def get_game_lines(self):
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
        except Exception as error:
            print(error)

        points = {}
        for game in result:
            for bookmaker in game['bookmakers']:
                if bookmaker['key'] == 'draftkings':
                    for market in bookmaker['markets']:
                        if market['key'] == 'spreads':
                            for outcome in market['outcomes']:
                                points[outcome["name"]] = outcome['point']
        print(f'{len(points)} NBA Game Odds loaded')
        return points
