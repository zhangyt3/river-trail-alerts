import logging
import jinja2
import os

log = logging.getLogger()
log.setLevel(logging.WARN)

searchpath="src/frontend/templates"

def subscribe_page():
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = templateEnv.get_template("index.html")

    page = template.render(os.environ['SUBSCRIBE_LAMBDA_ENDPOINT'])

    log.info(page)

    return page


def lambda_handler(event, context):
    email_address = event['body'].lstrip("userEmail=")

    print(f"Event: {email_address}")
    success = True
    
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
    
    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
        },
        'body': page
    }

