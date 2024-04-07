from datetime import date, timedelta
from model.NbaSeasonStats import NbaSeasonStats
from model.DailyScriptParameters import DailyScriptParameters
from model.Prediction import Prediction
from database.AwsTableDb import AwsTableDb
from utility.dates import dateToDashesString, slashesStringToDate, dateToSlashesString

class Database:
    def __init__(self):
        self.initializeconnection()
        self.getdailyscriptparameters()

    def initializeconnection(self) -> None:
        self.db: AwsTableDb = AwsTableDb()

    def getdailyscriptparameters(self) -> None:
        data = self.db.getTableConfig()

        try:
            parameters = DailyScriptParameters.from_json(data)
            print(f'Sucessfully Loaded: {parameters}')
        except:
            raise Exception(f'Parameters unable to be loaded')
        self.parameters = parameters
        self.year = parameters.seasonyear
        self.firstdayofseason = parameters.firstdayofseason
        self.startdate = parameters.startdate
        self.enddate = parameters.enddate

    def setdailyscriptparameters(self) -> None:
        self.parameters.enddate = dateToSlashesString(
            slashesStringToDate(self.parameters.enddate) + timedelta(days=1))
        self.parameters.startdate = self.parameters.enddate
        
        try:
            self.db.setTableConfig(self.parameters.to_json())
            print(f'Successfully Set: {self.parameters}')
        except:
            raise Exception(f'Parameters unable to be loaded')
    
    def GetTeamFromDatabase(self, teamname: str) -> NbaSeasonStats:
        try:
            result = self.db.getFromDb(teamname)
            print(f'{teamname} Successfully loaded from database')
        except:
            raise Exception(f'Get {teamname} Failed')

        if not result:
            return NbaSeasonStats(teamname, self.year)
        else:
            return NbaSeasonStats.from_json(result)

    def EditTeamInDatabase(self, teamname: str, 
                           seasonstats: NbaSeasonStats) -> None:
        try:
            self.db.addToDb(teamname, seasonstats.to_json())
            print(f'{teamname} Successfully Edited')
        except:
            raise Exception(f'Edit {teamname} Failed with: {seasonstats}')

    def GetAllTeamsFromDatabase(self) -> list[NbaSeasonStats]:
        try: 
            seasonstatslist: list[str] = self.db.getAllFromDbExceptConfig()
            print(f'{len(seasonstatslist)} teams retrieved from Database')
        except:
            raise Exception('Get All Teams Failed')

        seasonteamslist: list[NbaSeasonStats] = [
            NbaSeasonStats.from_json(team) for team in seasonstatslist]
        return seasonteamslist

    def EditAllTeamsInDatabase(self, 
                                seasonstatslist: list[NbaSeasonStats]) -> None:
        serializeddata: list[str] = [team.to_json() for team in seasonstatslist] 
        teamname: list[str] = [team.name for team in seasonstatslist]
        try:
            self.db.addItemsToDbBatch(teamname, serializeddata)
            print(f'{len(seasonstatslist)} edited in Database')
        except:
            raise Exception(f'Edit All Teams Failed With: {seasonstatslist}')

    def AddPredictions(self, date: date, predictions: list[Prediction]): 
        try:
            self.db.setPrediction(dateToDashesString(date), 
                [prediction.to_json() for prediction in predictions])
            print(f'{len(predictions)} Predictions Created in Database')
        except:
            raise Exception(f'Create Prediction Failed for {date} and {predictions}')
        
    def GetPredictionByDate(self, date: date) -> list[Prediction]: 
        dateDashes = dateToDashesString(date)
        try:
            results: list[str] = self.db.getPredictions(dateDashes)
            predictions = [ Prediction.from_json(res) for res in results]
            print(f'{len(predictions)} Predictions Retrieved from Database')
            return predictions
        except:
            raise Exception(f'Prediction Loading Failed for {dateDashes}')