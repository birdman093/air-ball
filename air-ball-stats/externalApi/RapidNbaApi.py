import requests, os, logging
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from model import NbaSeasonStats
from utility import dateToDashesString, convertUTCtoPSTtoDashesString

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class RapidNbaApi:
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
            raise Exception(f'N to retrieve API-NBA-V1 Games on {date}') from e
        return data
    