import json
import sys
import logging
import time, datetime
import pytz
from services import NbaDailyGamesService

logger = logging.getLogger('Airball-AWS-Lambda')
if not logger.handlers:
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

def handler(event, context):
    '''AWS Lambda Entry Point'''  
    start_time = time.time()   
    current_time = datetime.datetime.now(pytz.timezone(
        'America/Los_Angeles')).strftime('%m-%d-%Y')
    logger.info(f'AIR-BALL UPDATE STARTED at {current_time}')

    NbaDailyGamesService().update_game_stats_by_config()

    end_time = time.time()
    logger.info(f'AIR-BALL COMPLETED IN {end_time - start_time} secs')

    # *** DO NOT MODIFY TEXT BELOW *** AWS ALARM TAG ***
    logger.info('AIR-BALL UPDATE COMPLETED SUCCESSFULLY')

if __name__ == "__main__":
    handler(None, None)