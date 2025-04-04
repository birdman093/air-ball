import requests, os, logging
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from model import NbaSeasonStats
from utility import dateToDashesString, convertUTCtoPSTtoDashesString

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AirBallApi:
    def __init__(self):
        self.HOME = 'home'
        self.AWAY = 'away'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)
    
    def makePrediction(self, home: NbaSeasonStats, away: NbaSeasonStats,
                       date: date, mingames: int) -> dict:
        '''
        air-ball sample response -- 
        {"home_team_plus_minus_predictions":
        [{"home_team_plus_minus":1.6254919885342773}]}
        '''
        url = os.getenv('AIR_BALL_PREDICTION_URL') or ""
        payload = {"games" : [home.airballformat(True, date, mingames) 
                              | away.airballformat(False, date, mingames)]}
        
        try:
            response = requests.post(url, json=payload).json()
            prediction = response["home_team_plus_minus_predictions"][0]
            logger.info(f'Air-Ball Prediction: {away.name} @ {home.name}: {prediction}')
        except Exception as e:
            raise Exception(f'Failed to make prediction\n' +
                            f'url: {url}\n' +
                            f'payload: {payload}\n') from e


        return prediction
        
