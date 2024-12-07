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
from core.predictions import make_predictions_day, update_yesterdays_predictions
from core.rankings import update_season_rankings

MINGAMES = 10
SLEEPMODE = True
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def update_nba_games():
    ''' AWS Lambda Server Function - Runs Daily at 3am ET\n
    ** updates season data and prediction results using yesterdays games\n
    ** makes predictions for todays games\n
    ** updates configurations
    '''
    logging.info("** Update NBA Games Started **")

    db: Database = Database()
    nbaApi: NbaApi = NbaApi(db.year) 
    airBallApi: AirBallApi = AirBallApi()
    nbaBettingLine = NbaBettingLine()
    currentdate = slashesStringToDate(db.startdate) 
    enddate = slashesStringToDate(db.enddate) 
    if SLEEPMODE: time.sleep(1)

    while currentdate <= enddate:
        currentdategames: dict[str, dict[str, NbaGameStats]] = \
        nbaApi.get_played_games_on_date(dateToSlashesString(currentdate))

        yesterday_predictions: list[Prediction] = db.GetPredictionByDate(currentdate)
        air_ball_performance = AirBallPerformance()
        edit_teams = EditNbaSeasonStats(db.GetAllTeamsFromDatabase(), db.year)
        for game in currentdategames.values():
            if nbaApi.HOME not in game or nbaApi.AWAY not in game:
                continue
            home_game: NbaGameStats = game[nbaApi.HOME]
            away_game: NbaGameStats = game[nbaApi.AWAY]
            home_plus_minus = home_game.plus_minus;
            update_season_stats(home_game, away_game, edit_teams)

            # ** Update Yesterday's Predictions With Result **
            update_yesterdays_predictions(yesterday_predictions, 
                home_game.team_name, away_game.team_name, home_plus_minus, 
                air_ball_performance)

        # ** Add Predictions And Aggregate Stats to DB **     
        db.AddPredictions(currentdate, yesterday_predictions)
        db.EditAirBallPerformance(air_ball_performance)
        
        # ** Update Cumulative season Rankings in DB **
        edit_teams_list = edit_teams.get_team_list()
        update_season_rankings(edit_teams_list)

        # ** Save Edited Teams in DB **
        db.EditAllTeamsInDatabase(edit_teams_list)

        # ** Create Predictions for Today's Games **
        currentdate += timedelta(days=1)
        predictions = make_predictions_day(
            airBallApi, 
            nbaBettingLine, 
            EditNbaSeasonStats(edit_teams_list, db.year), currentdate)
        db.AddPredictions(currentdate, predictions)
        
    db.setdailyscriptparameters()
    logging.info("** Update NBA Games Completed **")

def update_season_stats(home_game: NbaGameStats, away_game: NbaGameStats, 
                        edit_teams: EditNbaSeasonStats):
    home_season: NbaSeasonStats = edit_teams.get_team(home_game.team_name)
    away_season: NbaSeasonStats = edit_teams.get_team(away_game.team_name)
    home_season.updateteamstats(home_game, True)
    home_season.updateopponentstats(away_game, away_season.rank)
    away_season.updateteamstats(away_game, False)
    away_season.updateopponentstats(home_game, home_season.rank)
    edit_teams.update_team(home_season)
    edit_teams.update_team(away_season)