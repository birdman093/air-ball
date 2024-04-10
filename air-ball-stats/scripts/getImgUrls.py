from database.Database import Database
from model.NbaSeasonStats import NbaSeasonStats

def getImgUrls():
    db: Database = Database()
    teams: list[NbaSeasonStats] = db.GetAllTeamsFromDatabase()
    for team in teams:
        print(f'\"{team.name}\":\"{team.logo_url}\",')