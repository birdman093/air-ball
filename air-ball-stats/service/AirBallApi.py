import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from model.NbaSeasonStats import NbaSeasonStats

class AirBallApi:
    def __init__(self):
        self.HOME = 'home'
        self.AWAY = 'away'
        load_dotenv('service/credentials/.env.local')

    def getGames(self, year, month, day) -> list[dict[str, str]]:
        '''
        All games on day
        '''
        date = datetime(year, month, day)
        next_day = date + timedelta(days=1)
        today_api_date = next_day.strftime('%Y-%m-%d')

        url = f"https://api-nba-v1.p.rapidapi.com/games?date={today_api_date}"
        headers = {
            'X-RapidAPI-Key': os.getenv('NEXT_PUBLIC_RAPIDAPI_KEY'),
            'X-RapidAPI-Host': os.getenv('NEXT_PUBLIC_RAPIDAPI_NBA_HOST')
        }
        response = requests.get(url, headers=headers)
        print(response.json())
        data = response.json()['response']

        games = []
        for game in data:
            hometeam = game['teams']['home']['name']
            awayteam = game['teams']['visitors']['name']
            print(f'{awayteam} @ {hometeam}')
            games.append({self.HOME : hometeam,
                          self.AWAY : awayteam})
        return games
    
    def makePrediction(self, home: NbaSeasonStats, away: NbaSeasonStats):
        '''
        air-ball response -- 
        {"home_team_plus_minus_predictions":
        [{"home_team_plus_minus":1.6254919885342773}]}
        '''
        url = "http://ec2-52-90-234-151.compute-1.amazonaws.com:8000/predict"
        payload = {"games" : [home.airballformat() | away.airballformat()]}
        response = requests.post(url, json=payload).json()
        return response["home_team_plus_minus_predictions"][0]["home_team_plus_minus"]
        
