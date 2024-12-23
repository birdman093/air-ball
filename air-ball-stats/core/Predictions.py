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
INVALID_BET = 999

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

        if hometeam.gamesplayed() >= MINGAMES and awayteam.gamesplayed() >= MINGAMES:
            prediction = airBallApi.makePrediction(
            hometeam, awayteam, currentdate, MINGAMES)
        else:
            prediction = {}
        
        hometeambettingline = INVALID_BET
        if currentdatedashes == todaydatedashes:
            hometeambettingline = get_betting_line(bettingline, hometeam.name)
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

def get_betting_line(bettingline: dict[str,float], teamname) -> float:
    line: float | None = bettingline.get(teamname)
    if not line and teamname in teamNameConversion:
        line = bettingline.get(teamNameConversion[teamname])
    if not line: return INVALID_BET
    return line

def check_valid_bet(line):
    return line != INVALID_BET


teamNameConversion = {
    "LA Clippers" : "Los Angeles Clippers"
}