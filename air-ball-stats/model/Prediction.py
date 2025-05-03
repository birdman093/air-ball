import json
from datetime import date
from utility import INVALID_PREDICTION, INVALID_RESULT

class Prediction:
    '''
    Predictions are based on home team plus/minus
    '''
    def __init__(self, hometeamname: str = "", hometeamgames: int = 0, 
                 awayteamname: str = "", awayteamgames: int = 0, 
                 hometeamprediction: float = INVALID_PREDICTION, hometeamlineodds: float = 0,
                 hometeaminput: str = "", awayteaminput: str = ""):
        self.hometeamname = hometeamname
        self.hometeamgames = hometeamgames
        self.awayteamname = awayteamname
        self.awayteamgames = awayteamgames
        self.hometeamplusminusprediction: float = hometeamprediction
        self.hometeamplusminusresult: float = INVALID_RESULT
        self.hometeamlineodds: float = hometeamlineodds
        self.hometeaminput = hometeaminput
        self.awayteaminput = awayteaminput

    def __str__(self):
        return (f"{self.awayteamname} @ {self.hometeamname} {self.hometeamplusminusprediction})")

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj
    