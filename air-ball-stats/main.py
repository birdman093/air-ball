'''
Kicks off on AWS at 3am
'''
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
from core.Predictions import MakePredictionsForDay

MINGAMES = 10

###### Server Update Script - Run daily at 3am #######
db: Database = Database()
nbaApi: NbaApi = NbaApi(db.year) 
airBallApi: AirBallApi = AirBallApi()
nbaBettingLine = NbaBettingLine()
currentdate = slashesStringToDate(db.startdate) 
enddate = slashesStringToDate(db.enddate) 
WINPCTTOLERANCE = .001

while currentdate <= enddate:
    currentdategames = nbaApi.getPlayedGamesOnDate(dateToSlashesString(currentdate))

    yesterday_predictions: list[Prediction] = db.GetPredictionByDate(currentdate)
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
            
    db.AddPredictions(currentdate, yesterday_predictions)
    
    # sos and rank daily cumulative stats
    team: NbaSeasonStats
    allteams: list[NbaSeasonStats] = db.GetAllTeamsFromDatabase()    
    allteams.sort(key=lambda team: team._winpct(), reverse=True) # sort highest
    previousteam = allteams[0] if len(allteams) > 0 else None
    rank = 1
    for idx, team in enumerate(allteams):
        if previousteam._winpct() - team._winpct() > WINPCTTOLERANCE:
            rank = idx + 1
        team.setrank(rank)
    db.EditAllTeamsInDatabase(allteams)

    currentdate += timedelta(days=1)

    # make predictions for next day
    MakePredictionsForDay(airBallApi, nbaBettingLine, db, currentdate)
    
#db.setdailyscriptparameters()
print("** Completed **")
