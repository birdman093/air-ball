#python
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
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

MINGAMES = 10

def MakePredictionsForDay(airBallApi : AirBallApi, 
                          nbaBettingLine: NbaBettingLine, 
                          db: Database, 
                          currentdate: date):
    print('*** Making Predictions ***')
    nextdaygames: list[dict[str,str]] = airBallApi.getUnPlayedGamesOnDate(currentdate)
    bettingline: dict = nbaBettingLine.get_game_lines()
    predictions: list[Prediction] = []
    todaydatedashes = dateToDashesString(get_today_date_PST())
    currentdatedashes = dateToDashesString(currentdate)
    print(nextdaygames)
    for game in nextdaygames:
        hometeam = db.GetTeamFromDatabase(game[airBallApi.HOME])
        awayteam = db.GetTeamFromDatabase(game[airBallApi.AWAY])
        prediction = airBallApi.makePrediction(
            hometeam, awayteam, currentdate, MINGAMES)
        hometeambettingline = 999
        if currentdatedashes == todaydatedashes:
            hometeambettingline = bettingline.get(hometeam.name)
            print(f'Added Betting Line for {awayteam.name} @ {hometeam.name} {hometeambettingline}')

        predictions.append(Prediction(
            hometeam.name, hometeam.gamesplayed(), 
            awayteam.name, awayteam.gamesplayed(),
            prediction, hometeambettingline,
            str(hometeam.airballformat(True, currentdate, MINGAMES)),
            str(awayteam.airballformat(False, currentdate, MINGAMES))))
        
    db.AddPredictions(
            currentdate, predictions)