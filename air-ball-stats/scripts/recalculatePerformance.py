from datetime import datetime, timedelta, date
from model import AirBallPerformance, Prediction
from databases import Database
from utility.dates import *

def recalculatePerformance(start_date: str, end_date: str, season_year: str):
    from services.prediction_service import PredictionService

    db: Database = Database()
    prediction_service: PredictionService = PredictionService(season_year)
    currentdate = slashesStringToDate(start_date) 
    enddate = slashesStringToDate(end_date) 
    ab_performance = AirBallPerformance()

    # update air-ball record
    while currentdate <= enddate:
        predictions: list[Prediction] = db.get_predictions_by_date_db(currentdate)
        for prediction in predictions:
            print(prediction)
            print(prediction.hometeamplusminusresult,
                    prediction.hometeamlineodds * -1, # reversal of odds 
                    prediction.hometeamplusminusprediction)
            if prediction_service.check_valid_prediction(prediction.hometeamplusminusprediction): 
                ab_performance.add_bet(
                    prediction.hometeamplusminusresult,
                    prediction.hometeamlineodds * -1, # reversal of odds 
                    prediction.hometeamplusminusprediction)

        currentdate += timedelta(days=1)

    #db.edit_air_ball_performance(ab_performance)
    print(ab_performance)
    