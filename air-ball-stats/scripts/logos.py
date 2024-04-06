from model.NbaSeasonStats import NbaSeasonStats
from database.Database import Database
from service.AirBallApi import AirBallApi
from datetime import date, datetime
from utility.dates import *
from datetime import date, datetime, timedelta

def add_logos() -> None:
    currentdate: date = get_today_date_PST() + timedelta(days=1)
    db: Database = Database()
    teams: int = 0
    MAX_TEAMS = 30
    counter = 0
    MAX_COUNTER = 5
    team: NbaSeasonStats
    allteams: list[NbaSeasonStats] = db.GetAllTeamsFromDatabase()
    allteams_dict: dict[str, NbaSeasonStats] = { team.name: team for team in allteams}

    while teams < MAX_TEAMS and counter < MAX_COUNTER:
        airBallApi: AirBallApi = AirBallApi()
        nextdaygames: list[dict[str,str]] = airBallApi.getUnPlayedGamesOnDate(currentdate)
        # NOTE -- Modified airBallApi function to store url
        for game in nextdaygames:
            hometeam = allteams_dict[game[airBallApi.HOME]]
            awayteam = allteams_dict[game[airBallApi.AWAY]]
            hometeam_url = game[airBallApi.HOME +'_url']
            awayteam_url = game[airBallApi.AWAY + '_url']
            if hometeam.logo_url == "" and len(hometeam_url) > 0: teams += 1
            if awayteam.logo_url == "" and len(awayteam_url) > 0: teams += 1
            hometeam.logo_url = hometeam_url
            awayteam.logo_url = awayteam_url

        counter += 1
        currentdate = currentdate + timedelta(days=1)

    db.EditAllTeamsInDatabase(allteams)
    print(f"Edited {teams} teams")