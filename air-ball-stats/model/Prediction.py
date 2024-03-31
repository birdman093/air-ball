import json
from datetime import date
from model.NbaSeasonStats import NbaSeasonStats

class Prediction:
    
    def __init__(self, hometeamname: str, hometeamgames: int, awayteamname: str,
                 awayteamgames: int, line: dict, prediction: dict,
                 hometeaminput: str, awayteaminput: str):
        self.hometeamname = hometeamname
        self.hometeamgames = hometeamgames
        self.awayteamname = awayteamname
        self.awayteamgames = awayteamgames
        self.plus_minus = "home_team_plus_minus"
        self.hometeamplusminusprediction = prediction[self.plus_minus]
        self.hometeam = hometeaminput
        self.awayteam = awayteaminput
        #self.hometeamplusminusline = line[self.plus_minus]

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
    