from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import logging

from model import EditNbaSeasonStats, Prediction, AirBallPerformance
from externalApi import NbaApi, AirBallApi, NbaBettingLineApi, RapidNbaApi
from utility import *

logger = logging.getLogger('PredictionService')

class PredictionService:
    def __init__(self, season_year):
        self.nbaApi = NbaApi(season_year)
        self.airBallApi = AirBallApi(MINIMUM_AIRBALL_GAMES)
        self.nbaBettingLine = NbaBettingLineApi()

    def make_predictions_day(self, teams: EditNbaSeasonStats, currentdate: date):
        logger.info(f'Starting for {currentdate}')
        nextdaygames = RapidNbaApi().getUnPlayedGamesOnDate(currentdate)
        bettingline = self.nbaBettingLine.get_game_lines()
        predictions = []
        todaydatedashes = dateToDashesString(get_today_date_PST())
        currentdatedashes = dateToDashesString(currentdate)
        for game in nextdaygames:
            hometeam = teams.get_team(game[HOME])
            awayteam = teams.get_team(game[AWAY])

            prediction = self.airBallApi.make_prediction(
            hometeam, awayteam, currentdate)
            
            home_team_line = INVALID_BET
            if currentdatedashes == todaydatedashes:
                home_team_line = self.get_betting_line(bettingline, hometeam.name)
                away_team_line = self.get_betting_line(bettingline, awayteam.name)
                if not self.nbaBettingLine.valid_game_lines(home_team_line, away_team_line):
                    logger.error(f'Conflicted Home/Away Lines - No Prediction created: {awayteam.name} @ {hometeam.name} home_team_line:{home_team_line} away_team_line:{away_team_line}')
                    home_team_line = INVALID_BET
                
            predictions.append(Prediction(
                hometeam.name, hometeam.gamesplayed(), 
                awayteam.name, awayteam.gamesplayed(),
                prediction, home_team_line,
                str(hometeam.airballformat(True, currentdate, MINIMUM_AIRBALL_GAMES)),
                str(awayteam.airballformat(False, currentdate, MINIMUM_AIRBALL_GAMES))))
        
        predictions_str = ', '.join(str(p) for p in predictions)
        logger.info(f'Created {len(predictions)} predictions on {currentdate} :[{predictions_str}]')
        return predictions

    def get_betting_line(self, bettingline: dict[str,float], teamname) -> float:
        line: float | None = bettingline.get(teamname)
        if not line and teamname in teamNameConversion:
            line = bettingline.get(teamNameConversion[teamname])
        if not line: return INVALID_BET
        return line

    def check_valid_bet(self, line):
        return line != INVALID_BET

    def update_yesterdays_predictions(self, yesterday_predictions: list[Prediction], 
            home_name: str, away_name: str, home_plus_minus: int,
            air_ball_performance: AirBallPerformance) -> None:
        for prediction in yesterday_predictions:
            if prediction.hometeamname == home_name and prediction.awayteamname == away_name:
                prediction.hometeamplusminusresult = home_plus_minus
                if self.check_valid_bet(prediction.hometeamplusminusprediction):
                    air_ball_performance.add_bet(
                        prediction.hometeamplusminusresult,
                        prediction.hometeamlineodds * -1,  # reversal of odds
                        prediction.hometeamplusminusprediction)
                    return                
        logger.info(f'PredictionService could not find prediction for {away_name} @ {home_name}')
