import logging
import boto3
import os
import json

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def send_updates(diffs):
    for location, prev, curr in diffs:
        log.debug(f'{location} changed from {prev} to {curr}')

    send_emails(boto3.client('sns'), diffs)

def form_email(diffs):
    return '\n'.join(
        [f'{loc} changed from {prev} to {curr}' for loc, prev, curr in diffs]
    )

def send_emails(client, diffs):
    message = form_email(diffs)
    response = client.publish(
        TargetArn=os.environ['EMAIL_SNS_TOPIC_ARN'],
        Message=json.dumps({
            'default': json.dumps(message),
            'email': form_email(diffs)
        }),
        Subject='River Trail Update',
        MessageStructure='json'
    )

