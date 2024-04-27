import json
import sys
import logging
from main import update_nba_games, test_working

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    '''AWS Lambda Entry Point'''
    logging.info('Started from handler')
    test_working()
    logging.info('Finished from handler')
    #update_nba_games