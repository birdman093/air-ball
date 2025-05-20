import json
import sys
import time, datetime
import pytz
from services import NbaDailyGamesService
from utility import log_info

logger_name = 'AWS Entry Point'

def handler(event, context):
    '''AWS Lambda Entry Point'''  
    start_time = time.time()   
    current_time = datetime.datetime.now(pytz.timezone(
        'America/Los_Angeles')).strftime('%m-%d-%Y')
    log_info(logger_name, f'AIR-BALL UPDATE STARTED at {current_time}')

    NbaDailyGamesService().update_game_stats_by_config()

    end_time = time.time()
    log_info(logger_name, f'AIR-BALL COMPLETED IN {end_time - start_time} secs')

    # *** DO NOT MODIFY TEXT BELOW *** AWS ALARM TAG ***
    log_info(logger_name,'AIR-BALL UPDATE COMPLETED SUCCESSFULLY')

if __name__ == "__main__":
    handler(None, None)