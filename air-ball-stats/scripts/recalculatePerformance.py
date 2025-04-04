from datetime import datetime, timedelta, date
from model.AirBallPerformance import AirBallPerformance
from model.Prediction import Prediction
from database.Database import Database
from services import PredictionService
from utility.dates import *

def recalculatePerformance(start_date: str, end_date: str, season_year: str):
    db: Database = Database()
    predictionService: PredictionService = PredictionService(season_year)
    currentdate = slashesStringToDate(start_date) 
    enddate = slashesStringToDate(end_date) 
    ab_performance = AirBallPerformance()

    # update air-ball record
    while currentdate <= enddate:
        predictions: list[Prediction] = db.get_predictions_by_date_db(currentdate)
        for prediction in predictions:
            if not predictionService.check_valid_bet(prediction.hometeamplusminusprediction): continue
            ab_performance.add_bet(
                prediction.hometeamplusminusresult,
                prediction.hometeamlineodds * -1, # reversal of odds 
                prediction.hometeamplusminusprediction)

        currentdate += timedelta(days=1)

    db.edit_air_ball_performance(ab_performance)
    print(ab_performance)

    