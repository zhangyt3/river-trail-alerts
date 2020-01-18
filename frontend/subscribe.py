import logging
import jinja2
import os
import boto3

from Environment import Environment

log = logging.getLogger()
log.setLevel(logging.INFO)

searchpath = "frontend/templates"

def subscribe_page(event, context):
    log.info(event)
    method = event['method']

    if method == 'GET':
        return render_sign_up_page()
    elif method == 'POST':
        return handle_subscription_create(event['body']['userEmail'])
    else:
        raise Exception(f"Invalid HTTP method {method}")

def handle_subscription_create(email):
    log.info(f'Creating new subscription for {email}')
    success = create_subscription(email)
    return render_signed_up_page(email, success)

def render_sign_up_page(env=Environment()):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )

    template = templateEnv.get_template("index.html")
    page = template.render(subscribe_url=env.get('SUBSCRIBE_LAMBDA_ENDPOINT'))
    
    return page

def render_signed_up_page(email_address, success):
    return_message = "Thanks for subscribing to River Trail Alerts!" if success \
        else "Sorry we could not subscribe you, please check if you are already subscribed or modify your email address."
    
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )

    template = templateEnv.get_template("subscription_return.html")
    page = template.render(
        return_message=return_message,
        email_address=email_address
    )
    
    log.info(page)
    return page

def create_subscription(email, env=Environment(), sns_client=boto3.client('sns')):
    """
    Adds a new SNS subscription for the given email.
    """
    sns_topic_arn = env.get('EMAIL_SNS_TOPIC_ARN')

    log.debug(f'Subscribing {email} to topic {sns_topic_arn}')
    response = sns_client.subscribe(
        TopicArn=sns_topic_arn,
        Protocol='email',
        Endpoint=email
    )
    log.debug(response)

    return response['SubscriptionArn'] == "pending confirmation"
