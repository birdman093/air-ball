from model.NbaSeasonStats import NbaSeasonStats
from AwsTableDb import AwsTableDb
from model.DailyScriptParameters import DailyScriptParameters

class Database:
    def __init__(self):
        self.initializeconnection()
        self.getdailyscriptparameters()

    def initializeconnection(self) -> None:
        self.db: AwsTableDb = AwsTableDb()

    def getdailyscriptparameters(self) -> None:
        data = self.db.getTableConfig()
        parameters = DailyScriptParameters.from_json(data)
        self.year = parameters.seasonyear
        self.firstdayofseason = parameters.firstdayofseason
        self.startdate = parameters.startdate
        self.enddate = parameters.enddate

    def setdailyscriptparameters(self, data: DailyScriptParameters) -> None:
        self.db.setTableConfig(data.to_json())
    
    def GetTeamFromDatabase(self, teamname: str) -> NbaSeasonStats:
        result = self.db.getFromDb(teamname)
        if not result:
            return NbaSeasonStats(teamname, self.year)

    def EditTeamInDatabase(self, teamname: str, 
                           seasonstats: NbaSeasonStats) -> None:
        self.db.addToDb(teamname, seasonstats.to_json())

    def GetAllTeamsFromDatabase(self, teamname: str) -> list[NbaSeasonStats]:
        seasonstatslist: list[str] = self.db.getAllFromDbExceptConfig()
        seasonteamslist: list[NbaSeasonStats] = [
            [NbaSeasonStats.to_json(team) for team in seasonstatslist]]
        return seasonteamslist

    def EditAllTeamsInDatabase(self, 
            teamname: list[str], seasonstatslist: list[NbaSeasonStats]) -> None:
        serializeddata: list[str] = [team.to_json() for team in seasonstatslist] 
        self.db.addItemsToDbBatch(teamname, serializeddata)

    def CreatePredictions(self, date, hometeam, awayteam, prediction): 
        pass

    def GetPredictions(self, date):
        pass