#python
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import logging
# internal 
from model.NbaGameStats import NbaGameStats
from model.NbaSeasonStats import NbaSeasonStats
from model.Prediction import Prediction
from database.Database import Database
from service.NbaApi import NbaApi
from service.AirBallApi import AirBallApi
from service.BettingLine import NbaBettingLine
from utility.dates import *
from scripts.logos import *  

logger = logging.getLogger()
logger.setLevel(logging.INFO)
MINGAMES = 10

def make_predictions_day(airBallApi : AirBallApi, 
                          nbaBettingLine: NbaBettingLine, 
                          db: Database, 
                          currentdate: date):
    logger.info('*** Start Make Predictions Day ***')
    nextdaygames: list[dict[str,str]] = airBallApi.getUnPlayedGamesOnDate(currentdate)
    bettingline: dict[str, float] = nbaBettingLine.get_game_lines()
    predictions: list[Prediction] = []
    todaydatedashes = dateToDashesString(get_today_date_PST())
    currentdatedashes = dateToDashesString(currentdate)
    logger.info(nextdaygames)
    for game in nextdaygames:
        hometeam = db.GetTeamFromDatabase(game[airBallApi.HOME])
        awayteam = db.GetTeamFromDatabase(game[airBallApi.AWAY])
        prediction = airBallApi.makePrediction(
            hometeam, awayteam, currentdate, MINGAMES)
        hometeambettingline = 999
        if currentdatedashes == todaydatedashes:
            hometeambettingline = bettingline.get(hometeam.name)
            if not hometeambettingline: hometeambettingline = 999
            logger.info(f'Prediction Created: {awayteam.name} @ {hometeam.name} {hometeambettingline}')
            
        predictions.append(Prediction(
            hometeam.name, hometeam.gamesplayed(), 
            awayteam.name, awayteam.gamesplayed(),
            prediction, hometeambettingline,
            str(hometeam.airballformat(True, currentdate, MINGAMES)),
            str(awayteam.airballformat(False, currentdate, MINGAMES))))
        
    db.AddPredictions(
            currentdate, predictions)
    logger.info('*** End Make Predictions Day ***')
