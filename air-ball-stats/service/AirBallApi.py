import requests, os, logging
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from model.NbaSeasonStats import NbaSeasonStats
from utility.dates import dateToDashesString, convertUTCtoPSTtoDashesString

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AirBallApi:
    def __init__(self):
        self.HOME = 'home'
        self.AWAY = 'away'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)

    def getUnPlayedGamesOnDate(self, date: date) -> list[dict[str, str]]:
        '''
        Get nba games by date\n  
        Return: [['home': {hometeamname}, 'away': {awayteamname}]]\n
        Accesses unplayed games only
        '''
        dayofgame = dateToDashesString(date)
        data = self.getGamesRequest(dayofgame) + \
        self.getGamesRequest(dateToDashesString(date + timedelta(days=1)))    
        games = []
        for game in data:
            gameday = convertUTCtoPSTtoDashesString(game['date']['start'])
            if gameday == dayofgame:
                hometeam = game['teams']['home']['name']
                awayteam = game['teams']['visitors']['name']
                logger.info(f'Added Unplayed Game: {awayteam} @ {hometeam}')
                games.append({self.HOME : hometeam,
                            self.AWAY : awayteam})
                            # f'{self.HOME}_url' : game['teams']['home']['logo'],
                            # f'{self.AWAY}_url' : game['teams']['visitors']['logo']})
        logger.info(f'{len(data)} API-NBA-V1 Games loaded for {date}')
        return games
    
    def getGamesRequest(self, date):
        url = f"https://api-nba-v1.p.rapidapi.com/games?date={date}"
        headers = {
            'X-RapidAPI-Key': os.getenv('NEXT_PUBLIC_RAPIDAPI_KEY'),
            'X-RapidAPI-Host': os.getenv('NEXT_PUBLIC_RAPIDAPI_NBA_HOST')
        }

        try: 
            response = requests.get(url, headers=headers)
            data = response.json()['response']
        except Exception as e: 
            raise Exception(f'Failed to retrieve API-NBA-V1 Games on {date}') from e
        return data
    
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
        
