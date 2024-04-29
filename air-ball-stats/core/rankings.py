#python
import logging
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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

WINPCTTOLERANCE = .001

def update_season_rankings(db: Database) -> None:
    logger.info('*** Start Update Season Rankings ***')
    team: NbaSeasonStats
    allteams: list[NbaSeasonStats] = db.GetAllTeamsFromDatabase()    
    allteams.sort(key=lambda team: team._winpct(), reverse=True) # sort highest
    previousteam = allteams[0] if len(allteams) > 0 else None
    if not previousteam: return
    rank = 1
    for idx, team in enumerate(allteams):
        if previousteam._winpct() - team._winpct() > WINPCTTOLERANCE:
            rank = idx + 1
        team.setrank(rank)
    db.EditAllTeamsInDatabase(allteams)
    logger.info('*** End Update Season Rankings ***')