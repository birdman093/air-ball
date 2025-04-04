import requests, os, logging
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from model import NbaSeasonStats
from utility import MINIMUM_AIRBALL_GAMES, INVALID_PREDICTION, HOME, AWAY

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AirBallApi:
    def __init__(self, min_games=MINIMUM_AIRBALL_GAMES):
        self.min_games = min_games
        self.HOME_TEAM_PLUS_MINUS_PREDICTIONS = 'home_team_plus_minus_predictions'
        self.HOME_TEAM_PLUS_MINUS = 'home_team_plus_minus'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)
    
    def make_prediction(self, home: NbaSeasonStats, away: NbaSeasonStats,
                       date: date) -> float:
        '''
        air-ball sample response -- {"home_team_plus_minus_predictions":
        [{"home_team_plus_minus":1.6254919885342773}]}
        '''
        if home.gamesplayed() < self.min_games or away.gamesplayed() < self.min_games:
            return INVALID_PREDICTION
        
        url = os.getenv('AIR_BALL_PREDICTION_URL') or ""
        payload = {"games" : [home.airballformat(True, date, self.min_games) 
                              | away.airballformat(False, date, self.min_games)]}
        
        try:
            response = requests.post(url, json=payload).json()
            prediction = response[self.HOME_TEAM_PLUS_MINUS][0].get(self.HOME_TEAM_PLUS_MINUS, INVALID_PREDICTION)
        except Exception as e:
            raise Exception(f'AirBallAPI failed to make prediction for {away.name} @ {home.name}\n' +
                            f'with payload: {payload}\n') from e

        return prediction
        
