from collections import defaultdict
import json, logging

WIN = "win"
LOSS = "loss"
TIE = "tie"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AirBallPerformance:
    def __init__(self):
        self.betting_diff_map: dict[str, dict[str, int]] = defaultdict(lambda: {WIN: 0, LOSS: 0, TIE: 0})
        self.overall_map = {WIN: 0, LOSS: 0, TIE: 0}

    def add_bet(self, result_line: float, game_line: float, prediction_line: float):
        rounded_bet_difference = round((prediction_line - game_line) * 2.0) / 2.0
        result_difference = result_line - game_line
        bet_win = (rounded_bet_difference > 0 and result_difference > 0) or \
        (rounded_bet_difference < 0 and result_difference < 0)
        str_res_diff = f"{rounded_bet_difference:.1f}"
        
        if bet_win: 
            self.betting_diff_map[str_res_diff][WIN] += 1
            self.overall_map[WIN] += 1
        elif result_difference == 0:
            self.betting_diff_map[str_res_diff][TIE] += 1
            self.overall_map[TIE] += 1
        else: 
            self.betting_diff_map[str_res_diff][LOSS] += 1
            self.overall_map[LOSS] += 1
        logger.info(f"Added Bet: Result:{bet_win}, Result-Line:{result_line}, Game-Line:{game_line}, Prediction: {prediction_line}")

    def merge_performance(self, merge_performance: 'AirBallPerformance'):
        for difference, performance in merge_performance.betting_diff_map.items():
            if difference not in self.betting_diff_map:
                self.betting_diff_map[difference] = {WIN: 0, LOSS: 0, TIE: 0}
            for key in [WIN, LOSS, TIE]:
                self.betting_diff_map[difference][key] += performance.get(key, 0)
        
        for key in [WIN, LOSS, TIE]:
            self.overall_map[key] += merge_performance.overall_map.get(key,0)
    
    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, data):
        obj = cls()
        obj.__dict__.update(data)
        return obj
    
    def __str__(self):
        return f"Air Ball Performance: W: {self.overall_map[WIN]} L: {self.overall_map[LOSS]} T: {self.overall_map[TIE]}"
        
