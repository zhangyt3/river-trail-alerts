import json
import os
import datetime
import logging

from model.StatusModel import StatusModel
from scrape.scraper import get_statuses
from notify.notifier import send_updates

from pprint import pprint

log = logging.getLogger()
log.setLevel(logging.WARN)


def get_previous_statuses(locations):
    statuses = dict()
    for l in locations:
        res = StatusModel.query(
            l,
            limit=1,
            scan_index_forward=False
        )
        res = res.next()

        statuses[res.pk] = res.status

    return statuses

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
    previous_statuses = get_previous_statuses(statuses.keys())
    diffs = find_diffs(previous_statuses, statuses)

    send_updates(diffs)
   
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    for location, is_open in statuses.items():
        status_model = StatusModel(pk=location, sk=time, status=is_open)
        status_model.save()

def handle(event, context):
    handle_update()
    
    print(f'SNS Topic ARN: {str(os.environ["EMAIL_SNS_TOPIC_ARN"])}')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

