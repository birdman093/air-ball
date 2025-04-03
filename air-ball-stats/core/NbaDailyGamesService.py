#python
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import time, logging
import requests
# internal 
from model.NbaGameStats import NbaGameStats
from model.NbaSeasonStats import NbaSeasonStats
from model.Prediction import Prediction
from model.AirBallPerformance import AirBallPerformance
from model.EditNbaSeasonStats import EditNbaSeasonStats
from database.Database import Database
from service.NbaApi import NbaApi
from service.AirBallApi import AirBallApi
from service.BettingLine import NbaBettingLine
from utility.dates import *
from scripts.logos import *
from core.PredictionService import make_predictions_day, update_yesterdays_predictions
from core.RankingsService import update_season_rankings

MINGAMES = 10
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class NbaDailyGamesService:
    def __init__(self):
        self.db: Database = Database()
        self.nbaApi: NbaApi = NbaApi(self.db.year) 
        self.airBallApi: AirBallApi = AirBallApi()
        self.nbaBettingLine = NbaBettingLine()

    def update_game_stats_by_config(self):
        ''' Updates Daily Games Using Dates from Config'''
        logging.info("** Update NBA Games Started **")
   
        current_date = slashesStringToDate(self.db.startdate) 
        end_date = slashesStringToDate(self.db.enddate) 

        while current_date <= end_date:
            self.update_daily_stats(current_date)
            
        self.db.setdailyscriptparameters()
        logging.info("** Update NBA Games Completed **")

    def update_daily_stats(self, current_date):
        '''
        Updates Daily NBA Game Stats and Predictions

        ** Updates Season Data and Prediction Results using yesterdays games **
        ** Makes Predictions for Todays Games **
        ** Updates Configurations
        '''
        air_ball_performance = AirBallPerformance()

        # ** Get Today's Games, Edit Teams, Yesterday's Predictions **
        current_date_games: dict[str, dict[str, NbaGameStats]] = \
        self.nbaApi.get_played_games_on_date(dateToSlashesString(current_date))
        previous_date_predictions: list[Prediction] = self.db.GetPredictionByDate(current_date)
        current_date_edit_teams = EditNbaSeasonStats(self.db.GetAllTeamsFromDatabase(), self.db.year)

        for game in current_date_games.values():
            # ** Update Game Result in Edit Teams Locally **
            if self.nbaApi.invalid_nba_game_stats(game): continue
            home_game, away_game = self.nbaApi.get_home_away_tuple(game)
            self.update_season_stats(home_game, away_game, current_date_edit_teams)

            # ** Update Yesterday's Predictions With Result **
            home_plus_minus = home_game.plus_minus
            update_yesterdays_predictions(previous_date_predictions, 
                home_game.team_name, away_game.team_name, home_plus_minus, 
                air_ball_performance)

        # ** Add Predictions And Aggregate Stats to DB **     
        self.db.AddPredictions(current_date, previous_date_predictions)
        self.db.EditAirBallPerformance(air_ball_performance)
        
        # ** Update Cumulative season Rankings in DB **
        edit_teams_list = current_date_edit_teams.get_team_list()
        update_season_rankings(edit_teams_list)

        # ** Save Edited Teams in DB **
        self.db.EditAllTeamsInDatabase(edit_teams_list)

        # ** Create Predictions for Today's Games **
        current_date += timedelta(days=1)
        predictions = make_predictions_day(
            self.airBallApi, 
            self.nbaBettingLine, 
            EditNbaSeasonStats(edit_teams_list, self.db.year), current_date)
        self.db.AddPredictions(current_date, predictions)

    def update_season_stats(self, home_game: NbaGameStats, away_game: NbaGameStats, 
                            edit_teams: EditNbaSeasonStats):
        home_season: NbaSeasonStats = edit_teams.get_team(home_game.team_name)
        away_season: NbaSeasonStats = edit_teams.get_team(away_game.team_name)
        home_season.updateteamstats(home_game, True)
        home_season.updateopponentstats(away_game, away_season.rank)
        away_season.updateteamstats(away_game, False)
        away_season.updateopponentstats(home_game, home_season.rank)
        edit_teams.update_team(home_season)
        edit_teams.update_team(away_season)