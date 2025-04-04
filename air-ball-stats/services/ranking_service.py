import logging
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

from model import NbaSeasonStats
from utility import *
from scripts.logos import *

logger = logging.getLogger('RankingService')

class RankingService:
    def __init__(self):
        pass

    def update_season_rankings(self, teams: list[NbaSeasonStats]) -> None:
        teams.sort(key=lambda team: team._winpct(), reverse=True) # sort highest
        previousteam = teams[0] if len(teams) > 0 else None
        if not previousteam: return
        rank = 1
        for idx, team in enumerate(teams):
            if previousteam._winpct() - team._winpct() > WINPCTTOLERANCE:
                rank = idx + 1
            team.setrank(rank)