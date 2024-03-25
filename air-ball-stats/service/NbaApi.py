from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
import pandas as pd

from model.NbaGameStats import NbaGameStats

class NbaApi:
    def __init__(self, year: str):
        self.year = year    #20XX-20XX
        self.LEAGUE = '00'  #NBA
        self.AWAY = 'away'
        self.HOME = 'home'

    def getgamesondate(self, date: str) -> dict[str, dict[str, NbaGameStats]]:
        '''
        Get nba games by date formatted #MO/DAY/YEAR  
        Return: gameid : {home : {stats}, away: {stats}}
        '''

        # TODO: Handle an error here
        currentdategames: pd.DataFrame = leaguegamefinder.LeagueGameFinder(
            league_id_nullable = self.LEAGUE,            
            season_nullable = self.year,        
            date_from_nullable = date,                                                 
            date_to_nullable = date).get_data_frames()[0]

        uniquegameids = {}
        for index, game in currentdategames.iterrows():
            teamside = self.AWAY if '@' in game['MATCHUP'] else self.HOME

            if game['GAME_ID'] not in uniquegameids:
                uniquegameids[game['GAME_ID']] = {}
            
            uniquegameids[game['GAME_ID']][teamside] = NbaGameStats(game)

        return uniquegameids
    
