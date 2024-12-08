#python
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import logging
# internal 
from model.NbaGameStats import NbaGameStats
from model.NbaSeasonStats import NbaSeasonStats
from model.EditNbaSeasonStats import EditNbaSeasonStats
from model.Prediction import Prediction
from model.AirBallPerformance import AirBallPerformance
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
                          teams: EditNbaSeasonStats, 
                          currentdate: date):
    logger.info('*** Start Make Predictions Day ***')
    nextdaygames: list[dict[str,str]] = airBallApi.getUnPlayedGamesOnDate(currentdate)
    bettingline: dict[str, float] = nbaBettingLine.get_game_lines()
    predictions: list[Prediction] = []
    todaydatedashes = dateToDashesString(get_today_date_PST())
    currentdatedashes = dateToDashesString(currentdate)
    logger.info(nextdaygames)
    for game in nextdaygames:
        hometeam = teams.get_team(game[airBallApi.HOME])
        awayteam = teams.get_team(game[airBallApi.AWAY])

        if hometeam.gamesplayed() >= MINGAMES and awayteam.gamesplayed() >= MINGAMES:
            prediction = airBallApi.makePrediction(
            hometeam, awayteam, currentdate, MINGAMES)
        else:
            prediction = {}
        
        home_team_line = INVALID_BET
        if currentdatedashes == todaydatedashes:
            home_team_line = get_betting_line(bettingline, hometeam.name)
            away_team_line = get_betting_line(bettingline, awayteam.name)
            if nbaBettingLine.invalid_game_lines(home_team_line, away_team_line):
                home_team_line = INVALID_BET
                logger.info(f'Conflicting Home/Away Lines Found - No Prediction Created: {awayteam.name} @ {hometeam.name} {home_team_line}')
            else:
                logger.info(f'Prediction Created: {awayteam.name} @ {hometeam.name} {home_team_line}')
            
        predictions.append(Prediction(
            hometeam.name, hometeam.gamesplayed(), 
            awayteam.name, awayteam.gamesplayed(),
            prediction, home_team_line,
            str(hometeam.airballformat(True, currentdate, MINGAMES)),
            str(awayteam.airballformat(False, currentdate, MINGAMES))))
        
    return predictions

def get_betting_line(bettingline: dict[str,float], teamname) -> float:
    line: float | None = bettingline.get(teamname)
    if not line and teamname in teamNameConversion:
        line = bettingline.get(teamNameConversion[teamname])
    if not line: return INVALID_BET
    return line

def check_valid_bet(line):
    return line != INVALID_BET

def update_yesterdays_predictions(yesterday_predictions: list[Prediction], 
        home_name: str, away_name: str, home_plus_minus: int,
        air_ball_performance: AirBallPerformance):
    for prediction in yesterday_predictions:
        if (
            prediction.hometeamname == home_name
            and prediction.awayteamname == away_name
            ):
            prediction.hometeamplusminusresult = home_plus_minus
            if check_valid_bet(prediction.hometeamplusminusprediction):
                air_ball_performance.add_bet(
                    prediction.hometeamplusminusresult,
                    prediction.hometeamlineodds * -1,  # reversal of odds
                    prediction.hometeamplusminusprediction,
            )


teamNameConversion = {
    "LA Clippers" : "Los Angeles Clippers"
}