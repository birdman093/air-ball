import json

class DailyScriptParameters:
    def __init__(self):
        self.seasonyear = '2023-24'
        self.firstdayofseason = True 
        self.startdate = '10/24/2023'
        self.enddate = '10/30/2023'

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def update_dates(self, startdate, enddate):
        self.firstdayofseason = False
        self.startdate = startdate
        self.enddate = enddate

    @classmethod
    def from_json(cls, json_str):
        print(f'Json String: {json_str}')
        if not json_str:
            return cls()
        data = json.loads(json_str)
        obj = cls()
        obj.__dict__.update(data)
        return obj
    
    def __str__(self):
        attributes = [f"{key} = {value}" for key, value in self.__dict__.items()]
        return f"DailyScriptParameters({', '.join(attributes)})"