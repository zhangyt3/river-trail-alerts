import json
import datetime

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pprint import pprint

from model.StatusModel import StatusModel
from scrape.scraper import get_statuses


def handle_update():
    statuses = get_statuses()

    # TODO retrieve previous statuses and compare

    # TODO send out any changes
    
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
    for location, is_open in statuses:
        status_model = StatusModel(pk=location, sk=time, status=is_open)
        status_model.save()

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

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

