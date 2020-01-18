import json
import os
import datetime
import logging

from model.StatusModel import StatusModel
from scrape.scraper import get_statuses
from notify.notifier import send_updates
from util import get_time, get_latest_statuses, save

from pprint import pprint

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def find_diffs(prev, curr):
    """
    Returns differences between previous and current status in the form
    (location, previous status, new status).
    """
    diffs = []

    for location, curr_status in curr.items():
        if prev[location] != curr_status:
            diffs.append((location, prev[location], curr_status))

    return diffs
    

def handle_update():
    statuses = get_statuses()
    previous_statuses = get_latest_statuses(statuses.keys())
    diffs = find_diffs(previous_statuses, statuses)
    log.debug(f'Changes: {diffs}')

    if diffs:
        send_updates(diffs)
    
    time = get_time()
    for location, status in statuses.items():
        save(location, time, status)

def handle(event, context):
    handle_update()
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

