from databases import Database
from model import NbaSeasonStats

def getImgUrls():
    db: Database = Database()
    teams: list[NbaSeasonStats] = db.get_all_teams_from_db()
    for team in teams:
        print(f'\"{team.name}\":\"{team.logo_url}\",')