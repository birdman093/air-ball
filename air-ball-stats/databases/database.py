from datetime import date, timedelta
from model import NbaSeasonStats, DailyScriptParameters, Prediction, AirBallPerformance
from .aws_dynamo_db import AwsDynamoDb
from utility import dateToDashesString, slashesStringToDate, dateToSlashesString, log_info, log_error

logger_name = 'Database'

class Database:
    def __init__(self, reset_parameters = False, dry_run = False):
        self.dry_run = dry_run
        if self.dry_run:
            log_info(logger_name, 'Running in dry-run mode')
        self.initialize_connection()
        if reset_parameters:
            self.reset_parameters()
        else:
            self.get_daily_parameters()

    def initialize_connection(self) -> None:
        self.db: AwsDynamoDb = AwsDynamoDb()

    def reset_parameters(self):
        log_info(logger_name, 'Resetting daily parameters')
        self.parameters = DailyScriptParameters()
        self.set_daily_parameters()

    def get_daily_parameters(self) -> None:
        data = self.db.getTableConfig()
        try:
            parameters = DailyScriptParameters.from_json(data)
            log_info(logger_name, f'Loaded Daily Parameters: {parameters}')
        except Exception as e:
            raise Exception('Database unable to load Daily Parameters') from e
        self.parameters = parameters
        self.year = parameters.seasonyear
        self.firstdayofseason = parameters.firstdayofseason
        self.startdate = parameters.startdate
        self.enddate = parameters.enddate

    def set_daily_parameters(self) -> None:
        self.parameters.enddate = dateToSlashesString(
            slashesStringToDate(self.parameters.enddate) + timedelta(days=1))
        self.parameters.startdate = self.parameters.enddate
        
        try:
            if not self.dry_run:
                self.db.setTableConfig(self.parameters.to_json())
            log_info(logger_name, f'Set Daily Parameters: {self.parameters}')
        except Exception as e:
            raise Exception('Database unable to set Daily Parameters') from e
    
    def get_team_from_db(self, teamname: str) -> NbaSeasonStats:
        try:
            result = self.db.getFromDb(teamname)
        except Exception as e:
            raise Exception(f'Database failed to get team: {teamname}') from e

        if not result:
            log_info(logger_name, f'Created team: {teamname} for {self.year}')
            return NbaSeasonStats(teamname, self.year)
        else:
            return NbaSeasonStats.from_json(result)

    def edit_team_in_db(self, teamname: str, 
                           seasonstats: NbaSeasonStats) -> None:
        try:
            if not self.dry_run:
                self.db.addToDb(teamname, seasonstats.to_json())
        except Exception as e:
            raise Exception(
                f'Database failed to edit team: {teamname} with stats: {seasonstats}') from e

    def get_all_teams_from_db(self) -> list[NbaSeasonStats]:
        try: 
            seasonstatslist: list[str] = self.db.getAllFromDbExceptConfig()
            log_info(logger_name, f'Loaded {len(seasonstatslist)} teams')
        except Exception as e:
            raise Exception('Database failed to get all teams') from e

        seasonteamslist: list[NbaSeasonStats] = [
            NbaSeasonStats.from_json(team) for team in seasonstatslist]
        return seasonteamslist

    def edit_all_teams_in_db(self, seasonstatslist: list[NbaSeasonStats]) -> None:
        serializeddata: list[str] = [team.to_json() for team in seasonstatslist] 
        teamname: list[str] = [team.name for team in seasonstatslist]
        try:
            if not self.dry_run:
                self.db.addItemsToDbBatch(teamname, serializeddata)
            log_info(logger_name, f'Edited {len(seasonstatslist)} teams')
        except Exception as e:
            raise Exception(f'Database failed to edit all teams: {seasonstatslist}') from e

    def create_predictions_db(self, date: date, predictions: list[Prediction]): 
        try:
            if not self.dry_run:
                self.db.setPrediction(dateToDashesString(date), 
                    [prediction.to_json() for prediction in predictions])
            log_info(logger_name, f'Created {len(predictions)} predictions for {date}')
        except Exception as e:
            raise Exception(
                f'Database failed to create preditions for {date}: {predictions}') from e
        
    def get_predictions_by_date_db(self, date: date) -> list[Prediction]: 
        dateDashes = dateToDashesString(date)
        try:
            results: list[str] = self.db.getPredictions(dateDashes)
            predictions = [ Prediction.from_json(res) for res in results]
            log_info(logger_name, f'Loaded {len(predictions)} predictions for {date}')
            return predictions
        except Exception as e:
            raise Exception(f'Failed to Load Predictions for {date}') from e
        
    def edit_air_ball_performance(self, air_ball_performance: AirBallPerformance):
        air_ball_json = self.db.getTablePerformance()
        air_ball_performance_db = AirBallPerformance().from_json(air_ball_json)
        air_ball_performance_db.merge_performance(air_ball_performance)
        try:
            if not self.dry_run:
                self.db.setTablePerformance(air_ball_performance_db.to_json())
            log_info(logger_name, f'Air Ball Performance updated {air_ball_performance_db}')
        except Exception as e:
            raise Exception('Database failed to edit Air Ball Performance') from e