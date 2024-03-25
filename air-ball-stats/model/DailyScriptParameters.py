import json

class DailyScriptParameters:
    def __init__(self):
        self.seasonyear = '2023-24'
        self.firstdayofseason = True 
        self.startdate = '10/24/2024'
        self.enddate = '10/24/2024'
        self.predictiondate = '10/25/2024'

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def update_dates(self, startdate, enddate, predictiondate):
        self.firstdayofseason = False
        self.startdate = startdate
        self.enddate = enddate
        self.predictiondate = predictiondate

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj