from model.AirBallPerformance import AirBallPerformance

def test_airballperformance():
    air_ball = AirBallPerformance()
    air_ball.from_json({})
    air_ball.add_bet(4.0, 13.0, 4.0) # W
    print(air_ball)
    air_ball.add_bet(16.0, 13.0, 4.0) # L
    print(air_ball)
    air_ball.add_bet(13.0, 13.0, 4.0) # T
    print(air_ball)

    # test writing and updating db
    #db = Database()
    #db.EditAirBallPerformance(air_ball)
    # {"betting_diff_map": {"-9.0": {"win": 1, "loss": 1, "tie": 1}}, 
    # "overall_map": {"win": 1, "loss": 1, "tie": 1}}