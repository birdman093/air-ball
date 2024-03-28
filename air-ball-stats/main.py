'''
Kicks off on AWS at 3am
'''
#python
import numpy as np, pandas as pd
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
# internal 
from model.NbaGameStats import NbaGameStats
from model.NbaSeasonStats import NbaSeasonStats
from model.Prediction import Prediction
from database.Database import Database
from service.NbaApi import NbaApi
from service.AirBallApi import AirBallApi
from utility.dates import *

###### Server Update Script - Run daily at 3am #######
db: Database = Database()
nbaApi: NbaApi = NbaApi(db.year) 
airBallApi: AirBallApi = AirBallApi()
currentdate = slashesStringToDate(db.startdate) 
enddate = slashesStringToDate(db.enddate) 
WINPCTTOLERANCE = .001

while currentdate <= enddate:
    currentdategames = nbaApi.getgamesondate(dateToSlashesString(currentdate))

    for game in currentdategames.values():
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
    nextdaygames: list[dict[str,str]] = airBallApi.getGames(currentdate)
    
    predictions: list[Prediction] = []
    for game in nextdaygames:
        hometeam = db.GetTeamFromDatabase(game[nbaApi.HOME])
        awayteam = db.GetTeamFromDatabase(game[nbaApi.AWAY])
        prediction = airBallApi.makePrediction(hometeam, awayteam, currentdate)
        predictions.append(Prediction(hometeam.name, awayteam.name, prediction))
        
    db.AddPredictions(
            currentdate, predictions)
    
#TODO: Update Daily Script Parameters
    
print("** Completed **")





