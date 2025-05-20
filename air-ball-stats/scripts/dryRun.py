from services import NbaDailyGamesService
from scripts import recalculatePerformance
import logging
import time, datetime
import pytz
from utility import log_info

'''
Test Whole Script
'''

def dryRunTest():
    # AWS handles basicConfig -- only use for testing
    logging.basicConfig(
        level=logging.INFO
    )

    logger_name = 'Airball-Testing'

    start_time = time.time()   
    current_time = datetime.datetime.now(pytz.timezone(
        'America/Los_Angeles')).strftime('%m-%d-%Y')
    log_info(logger_name,f'AIR-BALL UPDATE STARTED at {current_time}')
    NbaDailyGamesService(dry_run=True).update_game_stats_by_config()
    end_time = time.time()
    log_info(logger_name, f'AIR-BALL COMPLETED IN {end_time - start_time} secs')
    log_info(logger_name,'AIR-BALL UPDATE COMPLETED SUCCESSFULLY')


    ''' Recalculate Performance
    recalculatePerformance('03/01/2025', '03/31/2025', '2024-2025')
    '''