import os
import json
import logging
import requests

from model.StatusModel import StatusModel

log = logging.getLogger()
log.setLevel(logging.DEBUG)

VERIFY_TOKEN = "super-secret-token"


def verify(mode, token, challenge):
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            log.debug('Webhook verified')
            return 200, challenge
    return 404, None

def send_message(sender_psid, message):
    PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
    log.debug(f'Sending message to {sender_psid}')
    
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "recipient": {"id": sender_psid},
        "message": {
            "text": message
        }
    }

    response = requests.post(
        f'https://graph.facebook.com/v5.0/me/messages?access_token={PAGE_ACCESS_TOKEN}',
        headers=headers,
        data=json.dumps(body)
    )
    log.debug(response)

def handle_message(sender_psid, message):
    log.debug(f'Handling message from {sender_psid}: {message}')
    if 'text' in message:
        message = "TODO: parse message and return river trail status info"
        send_message(sender_psid, message)

def handle_messages(obj, entries):
    if obj != 'page':
        return 404
    
    for entry in entries:
        event = entry['messaging'][0]
        log.debug(event)
        
        sender_psid = event['sender']['id']
        if 'message' in event:
            message = event['message']
            handle_message(sender_psid, message)

    return 200    

def webhook(event, context):
    log.debug(event)
    method = event['httpMethod']

    status = None
    challenge = None
    if method == 'GET':
        req = event['queryStringParameters']
        mode = req['hub.mode']
        token = req['hub.verify_token']
        challenge = req['hub.challenge']
        status, challenge = verify(mode, token, challenge)
    elif method == 'POST':
        req = json.loads(event['body'])
        obj = req['object']
        entries = req['entry']
        status = handle_messages(obj, entries)
    else:
        log.error(f"Unsupported HTTP method: {method}")
    
    response = {"statusCode": status}
    if challenge:
        response['body'] = challenge
    
    return response
