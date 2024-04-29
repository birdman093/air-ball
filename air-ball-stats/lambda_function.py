import json
import sys
import logging
import time, datetime
import pytz
from core.update_nba_games import update_nba_games, test_working

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    '''AWS Lambda Entry Point'''
    start_time = time.time()
    current_time = datetime.datetime.now(pytz.timezone(
        'America/Los_Angeles')).strftime('%m-%d-%Y')
    logging.info(f"Started update_nba_games at {current_time}")
    #test_working()
    update_nba_games()
    end_time = time.time()
    logging.info(f'Finished update_nba_games inz {end_time - start_time} seconds')

    # *** DO NOT MODIFY *** AWS ALARM LOG ***
    logging.info('AIR-BALL UPDATE COMPLETED SUCCESSFULLY')

if __name__ == "__main__":
    handler(None, None)