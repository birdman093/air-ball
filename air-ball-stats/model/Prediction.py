import json
from datetime import date

class Prediction:
    def __init__(self, hometeamname: str, awayteamname: str,
                 prediction: dict):
        self.hometeamname = hometeamname
        self.awayteamname = awayteamname
        self.prediction = prediction

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj
    