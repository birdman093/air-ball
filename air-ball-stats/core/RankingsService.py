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

def update_season_rankings(teams: list[NbaSeasonStats]) -> None:
    teams.sort(key=lambda team: team._winpct(), reverse=True) # sort highest
    previousteam = teams[0] if len(teams) > 0 else None
    if not previousteam: return
    rank = 1
    for idx, team in enumerate(teams):
        if previousteam._winpct() - team._winpct() > WINPCTTOLERANCE:
            rank = idx + 1
        team.setrank(rank)