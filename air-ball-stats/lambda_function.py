import json
import sys
import logging
import time, datetime
import pytz
from services.NbaDailyGamesService import NbaDailyGamesService
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    '''AWS Lambda Entry Point'''
    start_time = time.time()
    current_time = datetime.datetime.now(pytz.timezone(
        'America/Los_Angeles')).strftime('%m-%d-%Y')
    logging.info(f"Started update_nba_games at {current_time}")
    # test_working()
    NbaDailyGamesService().update_game_stats_by_config()
    end_time = time.time()
    logging.info(f'Finished update_nba_games inz {end_time - start_time} seconds')

    # *** DO NOT MODIFY *** AWS ALARM TAG ***
    logging.info('AIR-BALL UPDATE COMPLETED SUCCESSFULLY')

if __name__ == "__main__":
    handler(None, None)