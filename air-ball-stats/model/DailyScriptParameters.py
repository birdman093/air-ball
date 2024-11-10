import json

class DailyScriptParameters:
    def __init__(self):
        '''
        Data Collection Configuration - Aggregates data for seasonyear from\n
        startdate to endate (inclusive) -- games must be completed for\n
        aggregation to occur correctly.

        startdate ### SET TO DAY BEFORE RUN DAY i.e. 10/21 will get results from
        10/21 and then get games yet to be played for 10/22
        '''
        self.seasonyear = '2024-25'
        self.firstdayofseason = True 
        self.startdate = '10/21/2024'  # 
        self.enddate = '10/22/2024'

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def update_dates(self, startdate, enddate):
        self.firstdayofseason = False
        self.startdate = startdate
        self.enddate = enddate

    @classmethod
    def from_json(cls, data):
        obj = cls()
        obj.__dict__.update(data)
        return obj
    
    def __str__(self):
        attributes = [f"{key} = {value}" for key, value in self.__dict__.items()]
        return f"DailyScriptParameters({', '.join(attributes)})"