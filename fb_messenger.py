import os
import json
import logging
import requests

from util import get_latest_statuses, get_all_trail_segments

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
        text = message['text'].lower()
        log.debug(text)

        segments_orig = get_all_trail_segments()
        segments = [segment.lower() for segment in segments_orig]
        log.debug(f'Segments from DB: {segments}')

        segments_in_text = []
        for segment in segments:
            if segment in text:
                segments_in_text.append(segment)

        message = None
        if segments_in_text:
            message = ""
            statuses = get_latest_statuses(segments_orig)
            for segment in segments:
                for name, status in statuses.items():
                    if segment == name.lower():
                        message += f"{Segment}: {status}\n"
        else:
            message = 'Send the name of a trail segment to see its status:\n\n' + '\n'.join(
                [f'\u2022 {seg}' for seg in segments]
            )

        send_message(sender_psid, message)

def handle_messages(obj, entries):
    if obj != 'page':
        return 404
    
    for entry in entries:
        if 'messaging' in entry:
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
