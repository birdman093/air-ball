from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import logging

from model import NbaGameStats, NbaSeasonStats,Prediction, AirBallPerformance, EditNbaSeasonStats
from database import Database
from externalApi import NbaApi,AirBallApi, NbaBettingLineApi
from services import PredictionService, RankingService
from utility import *
from scripts.logos import *

class NbaDailyGamesService:
    def __init__(self):
        self.db: Database = Database()
        self.nbaApi: NbaApi = NbaApi(self.db.year) 
        self.airBallApi: AirBallApi = AirBallApi(MINIMUM_AIRBALL_GAMES)
        self.nbaBettingLine = NbaBettingLineApi()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        self.predictionService = PredictionService(self.db.year)
        self.rankingService = RankingService()

    def update_game_stats_by_config(self):
        ''' Updates Daily Games Using Dates from Config'''
        logging.info("** Update NBA Games Started **")
   
        current_date = slashesStringToDate(self.db.startdate) 
        end_date = slashesStringToDate(self.db.enddate) 

        while current_date <= end_date:
            self.update_daily_stats(current_date)
            
        self.db.set_daily_parameters()
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
        previous_date_predictions: list[Prediction] = self.db.get_predictions_by_date_db(current_date)
        current_date_edit_teams = EditNbaSeasonStats(self.db.get_all_teams_from_db(), self.db.year)

        for game in current_date_games.values():
            # ** Update Game Result in Edit Teams Locally **
            if self.nbaApi.invalid_nba_game_stats(game): continue
            home_game, away_game = self.nbaApi.get_home_away_tuple(game)
            self.update_season_stats(home_game, away_game, current_date_edit_teams)

            # ** Update Yesterday's Predictions With Result **
            home_plus_minus = home_game.plus_minus
            self.predictionService.update_yesterdays_predictions(previous_date_predictions, 
                home_game.team_name, away_game.team_name, home_plus_minus, 
                air_ball_performance)

        # ** Add Predictions And Aggregate Stats to DB **     
        self.db.create_predictions_db(current_date, previous_date_predictions)
        self.db.edit_air_ball_performance(air_ball_performance)
        
        # ** Update Cumulative season Rankings in DB **
        edit_teams_list = current_date_edit_teams.get_team_list()
        self.rankingService.update_season_rankings(edit_teams_list)

        # ** Save Edited Teams in DB **
        self.db.edit_all_teams_in_db(edit_teams_list)

        # ** Create Predictions for Today's Games **
        current_date += timedelta(days=1)
        predictions = self.predictionService.make_predictions_day(
            EditNbaSeasonStats(edit_teams_list, self.db.year), current_date)
        self.db.create_predictions_db(current_date, predictions)

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