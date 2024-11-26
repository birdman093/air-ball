from datetime import datetime, timedelta, date
from model.AirBallPerformance import AirBallPerformance
from model.Prediction import Prediction
from database.Database import Database
from core.predictions import check_valid_bet
from utility.dates import *

def recalculatePerformance(start_date: str, end_date):
    db: Database = Database()
    currentdate = slashesStringToDate(start_date) 
    enddate = slashesStringToDate(end_date) 
    ab_performance = AirBallPerformance()

    # update air-ball record
    while currentdate <= enddate:
        predictions: list[Prediction] = db.GetPredictionByDate(currentdate)
        for prediction in predictions:
            if not check_valid_bet(prediction.hometeamplusminusprediction): continue
            ab_performance.add_bet(
                prediction.hometeamplusminusresult,
                prediction.hometeamlineodds * -1, # reversal of odds 
                prediction.hometeamplusminusprediction)

        currentdate += timedelta(days=1)

    db.EditAirBallPerformance(ab_performance)
    print(ab_performance)

    