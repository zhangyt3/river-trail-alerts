import logging
import jinja2
import os

log = logging.getLogger()
log.setLevel(logging.WARN)


def subscribe_page(measurements, searchpath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(
        loader=templateLoader,
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = templateEnv.get_template("index.html")

    page = template.render(os.environ[''])
    log.info(page)

    return page
import json


def subscribe_return(event, context):
    
    success = True
    
    return_message = "Thanks for subscribing to River Trail Alerts!" if success \
        else "Sorry we could not subscribe you, please check if you are already subscribed or modify your email address."
    
    
    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
        },
        'body':
            f'''<html>
              <head>
                <title>Winnipeg River Trail Alerts</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link
                  rel="stylesheet"
                  href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
                  integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
                  crossorigin="anonymous"
                />
                <link
                  rel="stylesheet"
                  href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
                  integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
                  crossorigin=""
                />
                <script
                  src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
                  integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
                  crossorigin=""
                ></script>
              </head>
              <body>
                    <div class="container">
                        <h1 class="display-3">{return_message}</h1>
                    </div>
              </body>
        </html>'''
    }
