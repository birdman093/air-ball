import json
from datetime import date
from utility import INVALID_PREDICTION

class Prediction:
    '''
    Predictions are based on home team plus/minus
    '''
    def __init__(self, hometeamname: str = "", hometeamgames: int = 0, 
                 awayteamname: str = "", awayteamgames: int = 0, 
                 hometeamprediction: float = INVALID_PREDICTION, hometeamlineodds: float = 0,
                 hometeaminput: str = "", awayteaminput: str = ""):
        self.home_name = hometeamname
        self.home_games_played = hometeamgames
        self.away_name = awayteamname
        self.away_games_played = awayteamgames
        self.home_prediction: float = hometeamprediction
        self.home_result: float = 0
        self.home_line: float = hometeamlineodds
        self.home_input = hometeaminput
        self.away_input = awayteaminput

    def __str__(self):
        return (f"{self.away_name} @ {self.home_name} {self.home_prediction})")

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj
    