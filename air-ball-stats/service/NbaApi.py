import logging
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
import pandas as pd
from datetime import date
from model.NbaGameStats import NbaGameStats

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class NbaApi:
    def __init__(self, year: str):
        self.year = year    #20XX-20XX
        self.LEAGUE = '00'  #NBA
        self.AWAY = 'away'
        self.HOME = 'home'

    def get_played_games_on_date(self, slashesDate: str) -> dict[str, dict[str, NbaGameStats]]:
        '''
        Get nba games by date formatted #MO/DAY/YEAR\n  
        Return: gameid : {home : {stats}, away: {stats}}\n
        Accesses PAST games only -- Not games yet to be played
        '''
        try: 
            currentdategames: pd.DataFrame = leaguegamefinder.LeagueGameFinder(
                league_id_nullable = self.LEAGUE,            
                season_nullable = self.year,        
                date_from_nullable = slashesDate,                                                 
                date_to_nullable = slashesDate).get_data_frames()[0]
            logger.info(f'{len(currentdategames)} teams loaded ' +
                  f'from LeagueGameFinder on {slashesDate}')
        except Exception as e:
            raise Exception(  
                f'NBA API failed: league_id_nullable = {self.LEAGUE}, ' +            
                f'season_nullable = {self.year}, ' +      
                f'date_from_nullable = {slashesDate}, ' +                                                
                f'date_to_nullable = {slashesDate}') from e

        uniquegameids = {}
        for _, game in currentdategames.iterrows():
            teamside = self.AWAY if '@' in game['MATCHUP'] else self.HOME

            if game['GAME_ID'] not in uniquegameids:
                uniquegameids[game['GAME_ID']] = {}
            
            uniquegameids[game['GAME_ID']][teamside] = NbaGameStats(game)
        
        logger.info(f'{len(uniquegameids)} games loaded ' +
                  f'from LeagueGameFinder on {slashesDate}')

        return uniquegameids
    
