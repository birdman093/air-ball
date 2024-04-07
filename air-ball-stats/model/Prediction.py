import json
from datetime import date
from model.NbaSeasonStats import NbaSeasonStats

class Prediction:
    def __init__(self, hometeamname: str = "", hometeamgames: int = 0, 
                 awayteamname: str = "", awayteamgames: int = 0, 
                 prediction: dict = {}, hometeamlineodds: float = 0,
                 hometeaminput: str = "", awayteaminput: str = ""):
        self.hometeamname = hometeamname
        self.hometeamgames = hometeamgames
        self.awayteamname = awayteamname
        self.awayteamgames = awayteamgames
        self.plus_minus: str = "home_team_plus_minus"
        self.hometeamplusminusprediction: float = prediction.get(self.plus_minus, 999)
        self.hometeamplusminusresult: float = 0
        self.hometeamlineodds: float = hometeamlineodds
        self.hometeaminput = hometeaminput
        self.awayteaminput = awayteaminput

    def __str__(self):
        return (f"Prediction(home: {self.hometeamname}," +
        f"away: {self.awayteamname}, prediction: {self.hometeamplusminus})")

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj
    