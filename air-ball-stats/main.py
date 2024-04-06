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
    nextdaygames: list[dict[str,str]] = airBallApi.getUnPlayedGamesOnDate(currentdate)
    bettingline: dict = nbaBettingLine.get_game_lines()
    predictions: list[Prediction] = []
    for game in nextdaygames:
        hometeam = db.GetTeamFromDatabase(game[nbaApi.HOME])
        awayteam = db.GetTeamFromDatabase(game[nbaApi.AWAY])
        prediction = airBallApi.makePrediction(
            hometeam, awayteam, currentdate, MINGAMES)
        
        currentdatedashes = dateToDashesString(currentdate)
        todaydatedashes = dateToDashesString(get_today_date_PST())
        if currentdatedashes == todaydatedashes:
            spreads = nbaBettingLine.get_game_lines()
            hometeambettingline = bettingline.get(spreads.get(hometeam.name))
            awayteambettingline = bettingline.get(spreads.get(awayteam.name))
            print(f'Added Betting Line for {awayteam.name} @ {hometeam.name}')
        else:
            hometeambettingline = ""
            awayteambettingline = ""

        predictions.append(Prediction(
            hometeam.name, hometeam.gamesplayed(), 
            awayteam.name, awayteam.gamesplayed(),
            prediction,
            str(hometeam.airballformat(True, currentdate, MINGAMES)),
            str(awayteam.airballformat(False, currentdate, MINGAMES)),
            hometeambettingline, awayteambettingline))
        
    db.AddPredictions(
            currentdate, predictions)
    
#db.setdailyscriptparameters()
print("** Completed **")





