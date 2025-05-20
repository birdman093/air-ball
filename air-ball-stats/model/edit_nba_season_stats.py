from .nba_season_stats import NbaSeasonStats
from utility import log_info

logger_name = 'EditNbaSeasonStats'

class EditNbaSeasonStats:
    def __init__(self, teams: list[NbaSeasonStats], year):
        self.team_dict = {team.name: team for team in teams}
        self.year = year

    def get_team(self, team_name: str) -> NbaSeasonStats:
        if team_name not in self.team_dict:
            log_info(logger_name, f'Team Created: {team_name}')
            return NbaSeasonStats(team_name, self.year)
        else:
            return self.team_dict[team_name]
        
    def update_team(self, team: NbaSeasonStats):
        self.team_dict[team.name] = team

    def get_team_list(self):
        return list(self.team_dict.values())


