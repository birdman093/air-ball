from datetime import date, timedelta
import logging
from model.NbaSeasonStats import NbaSeasonStats
from model.DailyScriptParameters import DailyScriptParameters
from model.Prediction import Prediction
from database.AwsTableDb import AwsTableDb
from utility.dates import dateToDashesString, slashesStringToDate, dateToSlashesString

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Database:
    def __init__(self, reset_parameters = False):
        self.initializeconnection()
        if reset_parameters:
            self.reset_parameters()
        else:
            self.getdailyscriptparameters()

    def initializeconnection(self) -> None:
        self.db: AwsTableDb = AwsTableDb()

    def reset_parameters(self):
        self.parameters = DailyScriptParameters()
        self.setdailyscriptparameters()

    def getdailyscriptparameters(self) -> None:
        data = self.db.getTableConfig()
        logger.info(data)

        try:
            parameters = DailyScriptParameters.from_json(data)
            logger.info(f'Daily Script Parameters Loaded: {parameters}')
        except Exception as e:
            raise Exception('ERROR: Daily Parameters unable to be loaded') from e
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
            logger.info(f'Daily Script Parameters Set: {self.parameters}')
        except Exception as e:
            raise Exception('ERROR: Daily Parameters unable to be set') from e
    
    def GetTeamFromDatabase(self, teamname: str) -> NbaSeasonStats:
        try:
            result = self.db.getFromDb(teamname)
            logger.info(f'Get Team: {teamname} loaded from database')
        except Exception as e:
            raise Exception(f'Get Team: {teamname} Failed') from e

        if not result:
            logger.info(f'Get Team - Team Created: {teamname} for {self.year}')
            return NbaSeasonStats(teamname, self.year)
        else:
            return NbaSeasonStats.from_json(result)

    def EditTeamInDatabase(self, teamname: str, 
                           seasonstats: NbaSeasonStats) -> None:
        try:
            self.db.addToDb(teamname, seasonstats.to_json())
            logger.info(f'Edit Team: {teamname}')
        except Exception as e:
            raise Exception(
                f'Edit Team: {teamname} Failed with: {seasonstats}') from e

    def GetAllTeamsFromDatabase(self) -> list[NbaSeasonStats]:
        try: 
            seasonstatslist: list[str] = self.db.getAllFromDbExceptConfig()
            logger.info(f'{len(seasonstatslist)} teams retrieved from Database')
        except Exception as e:
            raise Exception('Get All Teams Failed') from e

        seasonteamslist: list[NbaSeasonStats] = [
            NbaSeasonStats.from_json(team) for team in seasonstatslist]
        return seasonteamslist

    def EditAllTeamsInDatabase(self, 
                                seasonstatslist: list[NbaSeasonStats]) -> None:
        serializeddata: list[str] = [team.to_json() for team in seasonstatslist] 
        teamname: list[str] = [team.name for team in seasonstatslist]
        try:
            self.db.addItemsToDbBatch(teamname, serializeddata)
            logger.info(f'{len(seasonstatslist)} edited in Database')
        except Exception as e:
            raise Exception(f'Edit All Teams Failed: {seasonstatslist}') from e

    def AddPredictions(self, date: date, predictions: list[Prediction]): 
        try:
            self.db.setPrediction(dateToDashesString(date), 
                [prediction.to_json() for prediction in predictions])
            logger.info(f'{len(predictions)} Predictions Created in Database')
        except Exception as e:
            raise Exception(
                f'Failed to Create Prediction for {date} and {predictions}') from e
        
    def GetPredictionByDate(self, date: date) -> list[Prediction]: 
        dateDashes = dateToDashesString(date)
        try:
            results: list[str] = self.db.getPredictions(dateDashes)
            predictions = [ Prediction.from_json(res) for res in results]
            logger.info(f'{len(predictions)} Predictions Retrieved from Database')
            return predictions
        except Exception as e:
            raise Exception(f'Failed to Load Predictions for {dateDashes}') from e