import pandas as pd

class NbaGameStats:
    '''
    Game boxscore stats for team
    '''
    def __init__(self, df: pd.DataFrame):
        self.team_id = df['TEAM_ID']
        self.team_abbreviation = df['TEAM_ABBREVIATION']
        self.team_name: str = str(df['TEAM_NAME'])
        self.game_id = df['GAME_ID']
        self.game_date = df['GAME_DATE'] # YEAR-MO-DA e.g.2018-11-24
        self.matchup = df['MATCHUP']
        self.winloss: bool = True if df['WL'] == 'W' else False 
        self.minutes = df['MIN'] 
        self.pts = df['PTS']
        self.fgm = df['FGM']
        self.fga = df['FGA']
        self.fg_pct = df['FG_PCT']
        self.fg3m = df['FG3M']
        self.fg3a = df['FG3A']
        self.fg3_pct = df['FG3_PCT']
        self.ftm = df['FTM']
        self.fta = df['FTA']
        self.ft_pct = df['FT_PCT']
        self.oreb = df['OREB']
        self.dreb = df['DREB']
        self.reb = df['REB']
        self.ast = df['AST']
        self.stl = df['STL']
        self.blk = df['BLK']
        self.tov = df['TOV']
        self.pf = df['PF']
        self.plus_minus = df['PLUS_MINUS']
