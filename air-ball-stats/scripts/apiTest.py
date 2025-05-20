from model import NbaGameStats, NbaSeasonStats
from externalApi import NbaApi
from databases import Database
from datetime import date
from utility import dateToSlashesString, HOME, AWAY

def apiTestRun(game_date: date):
    nbaApi: NbaApi = NbaApi('2024-25') 
    games = nbaApi.get_played_games_on_date(dateToSlashesString(game_date))
    for game in games.values():
        if HOME not in game or AWAY not in game:
            continue
        home_game: NbaGameStats = game[HOME]
        away_game: NbaGameStats = game[AWAY]
        print(f'{away_game.team_name} @ {home_game.team_name}')
    
    