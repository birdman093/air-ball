from model.NbaGameStats import NbaGameStats
from model.NbaSeasonStats import NbaSeasonStats
from service.NbaApi import NbaApi
from database.Database import Database
from datetime import date
from utility.dates import dateToSlashesString

def reversal(teams: list[str], game_date: date):
    ''' Reverse last entry for team using NbaSeasonStats reversal methods'''
    print(f'Starting Reversal for ({len(teams)}) {teams} for {game_date}')
    db: Database = Database()
    nbaApi: NbaApi = NbaApi(db.year) 
    games = nbaApi.get_played_games_on_date(dateToSlashesString(game_date))
    reversed = 0
    for game in games.values():
        if nbaApi.HOME not in game or nbaApi.AWAY not in game:
            continue
        home_game: NbaGameStats = game[nbaApi.HOME]
        away_game: NbaGameStats = game[nbaApi.AWAY]
        home_season: NbaSeasonStats = db.GetTeamFromDatabase(home_game.team_name)
        away_season: NbaSeasonStats = db.GetTeamFromDatabase(away_game.team_name)
        if home_season.name in teams:
            home_season._reverseteamstats(home_game, True)
            home_season._reverseopponentstats(away_game, away_season.rank)
            db.EditTeamInDatabase(home_game.team_name, home_season)
            reversed += 1
        if away_season.name in teams:
            away_season._reverseteamstats(away_game, False)
            away_season._reverseopponentstats(home_game, home_season.rank)
            db.EditTeamInDatabase(away_game.team_name, away_season)
            reversed += 1

    print(f'Reversed {len(teams)} teams')
    
if __name__ == "__main__":
    teams = teams = [
    "San Antonio Spurs",
    "Utah Jazz",
    "LA Clippers",
    "Toronto Raptors",
    "Cleveland Cavaliers",
    "Brooklyn Nets",
    "Atlanta Hawks",
    "Chicago Bulls"
    ]
    reversal(teams, date(2024, 11, 9))
    