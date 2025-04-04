import json
from datetime import date, datetime

from .nba_game_stats import NbaGameStats
from utility import dashesStringToDate, safe_divide, HOME, AWAY

class NbaSeasonStats:
    '''
    Cumulative Season Stats by Team and Year up-to-date
    '''
    def __init__(self, name: str, year: str):
        # identifiers
        self.name: str = name
        self.year: str = year
        self.abbreviation: str = ''
        self.logo_url: str = ''

        # cumulative stats
        self.wins: int = 0
        self.losses: int = 0
        self.rank: int = 16

        # team cumulative stats
        self._3pm: int = 0
        self._3pa: int = 0
        self._2pm: int = 0
        self._2pa: int = 0
        self.pts: int = 0
        self.to: int = 0
        self.poss: int = 0
        self.orb: int = 0
        self.drb: int = 0

        # opponent cumulative stats
        self.opp_3pm: int = 0
        self.opp_3pa: int = 0
        self.opp_2pm: int = 0
        self.opp_2pa: int= 0
        self.opp_pts: int = 0
        self.opp_to: int = 0
        self.opp_poss: int = 0
        self.opp_orb: int = 0
        self.opp_drb: int = 0

        # cumulative game stats
        self.gamedates: list[str] = [] #game, YEAR-MO-DA e.g.2018-11-24
        self.opponent: list[str] = [] #game
        self.washometeam: list[bool] = [] #game
        self.waswinner: list[bool] = [] # game
        self.sos: list[int] = [] # game
        self.ranks: list[int] = [] # daily

    def updateteamstats(self, stats: NbaGameStats, hometeam: bool):
        if self.gamesplayed() == 0: self.abbreviation = stats.team_abbreviation
        
        if stats.winloss: self.wins += 1
        else: self.losses += 1

        # team cumulative stats
        self._3pm += stats.fg3m
        self._3pa += stats.fg3a
        self._2pm += stats.fgm - stats.fg3m
        self._2pa += stats.fga - stats.fg3a
        self.pts += stats.pts
        self.to += stats.tov
        self.poss += stats.fga - stats.oreb + stats.tov + stats.fta/2
        self.orb += stats.oreb
        self.drb += stats.dreb

        self.gamedates.append(stats.game_date)
        self.washometeam.append(hometeam)
        self.waswinner.append(stats.winloss)

    def updateopponentstats(self, stats: NbaGameStats, opp_rank: int):
        self.opp_3pm += stats.fg3m
        self.opp_3pa += stats.fg3a
        self.opp_2pm += stats.fgm - stats.fg3m
        self.opp_2pa += stats.fga - stats.fg3a
        self.opp_pts += stats.pts
        self.opp_to += stats.tov
        self.opp_poss += stats.fga - stats.oreb + stats.tov + stats.fta/2
        self.opp_orb += stats.oreb
        self.opp_drb += stats.dreb

        self.opponent.append(stats.team_name)
        self.sos.append(opp_rank)

    def setrank(self, newrank):
        self.rank = newrank
        self.ranks.append(newrank)

    def gamesplayed(self) -> int:
        return self.wins + self.losses

    def _restdays(self, date: date) -> int:
        '''
        Days off between games --> capped at 1
        '''
        MAX_REST = 1
        if len(self.gamedates) == 0: return 1
        lastgame_date_str = self.gamedates[-1]
        lastgame_date = dashesStringToDate(lastgame_date_str)
        return max((date - lastgame_date).days - 1, MAX_REST)
    
    def _homeprior(self) -> int:
        '''
        Previous game was home? -> return 1 if home, 0 if away
        '''
        return 1 if self.gamesplayed() > 0 and self.washometeam[-1] else 0
    
    def _sos(self, avggames = 100) -> float:
        '''
        Strength of Schedule - Average rank of teams by _winpct() over numgames
        '''
        avggames = min(avggames, self.gamesplayed())
        totalgames = len(self.sos)
        if avggames == 0 or totalgames == 0: return 16
        total_sos = sum(self.sos[i] for i in range(totalgames - avggames, totalgames))
        return total_sos / avggames

    def _winpct(self, calculationgames = 100) -> float:
        playedgames = self.gamesplayed()
        calculationgames = min(calculationgames, playedgames)
        if calculationgames == 0 or playedgames == 0: return 1 # 100% win pct
        total_wins = sum(1 if self.waswinner[i] == True else 0 for i in range(playedgames - calculationgames, playedgames))
        return total_wins / calculationgames

    def _3ptpct(self) -> float: 
        return safe_divide(self._3pm, self._3pa)
    
    def _opp_3ptpct(self) -> float: 
        return safe_divide(self.opp_3pm, self.opp_3pa)

    def _2ptpct(self) -> float:
        return safe_divide(self._2pm, self._2pa)
    
    def _opp_2ptpct(self) -> float:
        return safe_divide(self.opp_2pm, self.opp_2pa)
    
    def _pp100pp(self) -> float:
        return 100 * (safe_divide(self.pts, self.poss))
    
    def _opp_pp100pp(self) -> float:
        return 100 * (safe_divide(self.opp_pts, self.opp_poss))
    
    def _orbpct(self) -> float:
        return safe_divide(self.orb, (self._2pm + self._3pm))
    
    def _drbpct(self) -> float:
        return safe_divide(self.drb, self._opp_missed_shots())
    
    def _efgpct(self) -> float:
        return safe_divide((1.5 * self._3pm + self._2pm), (self._3pa + self._2pa))

    def _opp_efgpct(self) -> float:
        return safe_divide((1.5 * self.opp_3pm + self.opp_2pm),(self.opp_3pa + self.opp_2pa))
    
    def _opp_missed_shots(self) -> int:
        return self.opp_3pa + self.opp_2pa - self.opp_3pm - self.opp_2pm

    def airballformat(self, hometeam: bool, date: date, mingames: int) -> dict:
        ''' Project Air-Ball API Formatting '''
        location = HOME if hometeam else AWAY
        
        return { f"{location}_team_days_rest": self._restdays(date),
                f"{location}_team_home_prior": self._homeprior(),
                f"{location}_team_sos": self._sos(),
                f"{location}_team_sos_last_10": self._sos(mingames), 
                f"{location}_team_win_pct": self._winpct(), 
                f"{location}_team_win_pct_last_10": self._winpct(mingames), 
                f"{location}_team_3pt_pct": self._3ptpct(), 
                f"{location}_team_2pt_pct": self._2ptpct(), 
                f"{location}_team_pp100p": self._pp100pp(), 
                f"{location}_team_orb_pct": self._orbpct(), 
                f"{location}_team_drb_pct": self._drbpct(), 
                f"{location}_team_opp_3pt_pct": self._opp_3ptpct(), 
                f"{location}_team_opp_2pt_pct": self._opp_2ptpct(), 
                f"{location}_team_opp_pp100p": self._opp_pp100pp()
                }
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def update_dates(self, startdate, enddate, predictiondate):
        self.firstdayofseason = False
        self.startdate = startdate
        self.enddate = enddate
        self.predictiondate = predictiondate

    @classmethod
    def from_json(cls, json_dict):
        obj = cls(json_dict['name'], json_dict['year'])
        obj.__dict__.update(json_dict)
        return obj
    
    # ******* for reversal usage only ********
    
    def _reverseteamstats(self, stats: NbaGameStats, hometeam: bool):
        if stats.winloss: self.wins -= 1
        else: self.losses -= 1

        # team cumulative stats
        self._3pm -= stats.fg3m
        self._3pa -= stats.fg3a
        self._2pm -= stats.fgm - stats.fg3m
        self._2pa -= stats.fga - stats.fg3a
        self.pts -= stats.pts
        self.to -= stats.tov
        self.poss -= stats.fga - stats.oreb + stats.tov + stats.fta/2
        self.orb -= stats.oreb
        self.drb -= stats.dreb

        self.gamedates.pop()
        self.washometeam.pop()
        self.waswinner.pop()

    def _reverseopponentstats(self, stats: NbaGameStats, opp_rank: int):
        self.opp_3pm -= stats.fg3m
        self.opp_3pa -= stats.fg3a
        self.opp_2pm -= stats.fgm - stats.fg3m
        self.opp_2pa -= stats.fga - stats.fg3a
        self.opp_pts -= stats.pts
        self.opp_to -= stats.tov
        self.opp_poss -= stats.fga - stats.oreb + stats.tov + stats.fta/2
        self.opp_orb -= stats.oreb
        self.opp_drb -= stats.dreb

        self.opponent.pop()
        self.sos.pop()
