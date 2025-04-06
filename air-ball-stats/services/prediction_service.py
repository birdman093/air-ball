from datetime import datetime, timedelta, date
import math
from dotenv import load_dotenv
import logging

from model import EditNbaSeasonStats, Prediction, AirBallPerformance, NbaGameStats
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

    def check_valid_prediction(self, line: float):
        return not math.isclose(line, INVALID_PREDICTION)

    def update_yesterdays_predictions(self, 
        yesterday_predictions: list[Prediction], 
        home_game: NbaGameStats, away_game: NbaGameStats, 
        air_ball_performance: AirBallPerformance) -> None:

        # matching prediction to game results
        game_predictions = [
        prediction
        for prediction in yesterday_predictions
        if prediction.home_name == home_game.team_name
        and prediction.away_name == away_game.team_name
        ]
        yesterday_prediction = game_predictions[0] if len(game_predictions) > 0 else None

        # updating yesterdays prediction and air-ball-performance
        if yesterday_prediction and self.check_valid_prediction(yesterday_prediction.home_prediction) \
            and self.check_valid_prediction(yesterday_prediction.home_line) \
                and self.check_valid_prediction(home_game.plus_minus):
            yesterday_prediction.home_result = home_game.plus_minus
            air_ball_performance.add_bet(
                yesterday_prediction.home_result,
                yesterday_prediction.home_line * -1,  # reversal of odds
                yesterday_prediction.home_prediction)
        elif yesterday_prediction:
            yesterday_prediction.home_result = home_game.plus_minus
            logger.info(f'PredictionService found an invalid prediction for' +
                        f'{away_game.team_name} @ {home_game.team_name}')  
        else:                
            logger.info(f'PredictionService unable to find prediction for' +
                        f'{away_game.team_name} @ {home_game.team_name}')
