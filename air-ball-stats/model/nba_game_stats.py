import pandas as pd

class NbaGameStats:
    '''
    Game boxscore stats for team
    '''
    def __init__(self, df: pd.DataFrame):
        self.team_id = df['TEAM_ID'].iloc[0]
        self.team_abbreviation = df['TEAM_ABBREVIATION'].iloc[0]
        self.team_name: str = str(df['TEAM_NAME'].iloc[0])
        self.game_id = df['GAME_ID'].iloc[0]
        self.game_date = df['GAME_DATE'].iloc[0] # YEAR-MO-DA e.g.2018-11-24
        self.matchup = df['MATCHUP'].iloc[0]
        self.winloss: bool = df['WL'].iloc[0] == 'W'
        self.minutes = df['MIN'].iloc[0] 
        self.pts = df['PTS'].iloc[0]
        self.fgm = df['FGM'].iloc[0]
        self.fga = df['FGA'].iloc[0]
        self.fg_pct = df['FG_PCT'].iloc[0]
        self.fg3m = df['FG3M'].iloc[0]
        self.fg3a = df['FG3A'].iloc[0]
        self.fg3_pct = df['FG3_PCT'].iloc[0]
        self.ftm = df['FTM'].iloc[0]
        self.fta = df['FTA'].iloc[0]
        self.ft_pct = df['FT_PCT'].iloc[0]
        self.oreb = df['OREB'].iloc[0]
        self.dreb = df['DREB'].iloc[0]
        self.reb = df['REB'].iloc[0]
        self.ast = df['AST'].iloc[0]
        self.stl = df['STL'].iloc[0]
        self.blk = df['BLK'].iloc[0]
        self.tov = df['TOV'].iloc[0]
        self.pf = df['PF'].iloc[0]
        self.plus_minus: int = df['PLUS_MINUS'].iloc[0]
