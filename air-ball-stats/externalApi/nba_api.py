import os
from dotenv import load_dotenv
import pandas as pd
from datetime import date

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from model import NbaGameStats
from utility import HOME, AWAY, log_info, log_error

logger_name = 'NbaApi'

class NbaApi:
    def __init__(self, year: str):
        self.year = year    #20XX-20XX
        self.LEAGUE = '00'  #NBA
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)
        username = os.getenv('PROXY_USERNAME') or ""
        password = os.getenv('PROXY_PASSWORD') or ""
        port = os.getenv('PROXY_PORT') or ""
        self.proxy = f"http://{username}:{password}@gate.smartproxy.com:{port}"

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
                date_to_nullable = slashesDate,
                proxy = self.proxy).get_data_frames()[0]
        except Exception as e:
            raise Exception(  
                f'NbaApi failed to load: league_id_nullable = {self.LEAGUE}, ' +            
                f'season_nullable = {self.year}, ' +      
                f'date_from_nullable = {slashesDate}, ' +                                                
                f'date_to_nullable = {slashesDate}') from e

        uniquegameids = {}
        for _, game in currentdategames.iterrows():
            teamside = AWAY if '@' in game['MATCHUP'] else HOME

            if game['GAME_ID'] not in uniquegameids:
                uniquegameids[game['GAME_ID']] = {}
            
            uniquegameids[game['GAME_ID']][teamside] = NbaGameStats(game.to_frame().T)
        
        log_info(logger_name, f'Loaded {len(uniquegameids)} games from {slashesDate}')
        log_info(logger_name, ", ".join(f"{game}: {home}, {away}" for game, (home, away) in uniquegameids.items()))
    
        for game in uniquegameids.values():
            if self.invalid_nba_game_stats(game):
                log_error(logger_name, f'** Non-Breaking ** Failed to load game: {game}')
                del uniquegameids

        return uniquegameids
    
    # TODO: use Nba API scoreboard endpoint for todays games

    # TODO: create function to use scoreboard for today, and game finder for past dates
    
    def invalid_nba_game_stats(self, game: dict[str, NbaGameStats]) -> bool:
        return HOME not in game or AWAY not in game
    
    def get_home_away_tuple(self, game: dict[str, NbaGameStats]) -> tuple[NbaGameStats, NbaGameStats]:
        return (game[HOME], game[AWAY])
        
