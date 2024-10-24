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
from database.Database import Database
from service.NbaApi import NbaApi
from service.AirBallApi import AirBallApi
from service.BettingLine import NbaBettingLine
from utility.dates import *
from scripts.logos import *
from core.predictions import make_predictions_day
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
        currentdategames = nbaApi.get_played_games_on_date(dateToSlashesString(currentdate))

        yesterday_predictions: list[Prediction] = db.GetPredictionByDate(currentdate)
        air_ball_performance = AirBallPerformance()
        for game in currentdategames.values():
            # update daily stats
            home_game: NbaGameStats = game[nbaApi.HOME]
            away_game: NbaGameStats = game[nbaApi.AWAY]
            home_season: NbaSeasonStats = db.GetTeamFromDatabase(home_game.team_name)
            away_season: NbaSeasonStats = db.GetTeamFromDatabase(away_game.team_name)
            home_season.updateteamstats(home_game, True)
            home_season.updateopponentstats(away_game, away_season.rank)
            away_season.updateteamstats(away_game, False)
            away_season.updateopponentstats(home_game, home_season.rank)
            db.EditTeamInDatabase(home_game.team_name, home_season)
            db.EditTeamInDatabase(away_game.team_name, away_season)

            # update yesterday's predictions
            for prediction in yesterday_predictions:
                if prediction.hometeamname == home_game.team_name \
                and prediction.awayteamname == away_game.team_name:
                    prediction.hometeamplusminusresult = home_game.plus_minus
                    air_ball_performance.add_bet(prediction.hometeamplusminusresult,
                                                 prediction.hometeamlineodds,
                                                 prediction.hometeamplusminusprediction)
            
        if SLEEPMODE: time.sleep(len(currentdategames))      
        db.AddPredictions(currentdate, yesterday_predictions)
        if SLEEPMODE: time.sleep(len(currentdategames))
        db.EditAirBallPerformance(air_ball_performance)
        if SLEEPMODE: time.sleep(len(currentdategames))
        
        # sos and rank daily cumulative stats
        update_season_rankings(db)
        if SLEEPMODE: time.sleep(30)

        # make predictions for next day
        currentdate += timedelta(days=1)
        make_predictions_day(airBallApi, nbaBettingLine, db, currentdate)
        
    db.setdailyscriptparameters()
    logging.info("** Update NBA Games Completed **")

def test_working():
    # NBA API test
    nbaApi = NbaApi("2023-24")
    logging.info(nbaApi.get_played_games_on_date("04/28/2024"))

    # DB test
    db = Database()
    knicks = db.GetTeamFromDatabase("New York Knicks")
    logging.info(f"Retrieved data: {knicks}")
