import logging

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Filter out <li> elements with these texts inside during parsing
IGNORE = set([
    'Open',
    'Closed',
    'Conditions variable'
])

# The <svg> elements on the page have these classes when a location is open/closed/conditions variable
OPEN = 'check'
CLOSED = 'closed'
CONDITIONS_VARIABLE = 'dash'

# <li> elements that are headings have this class attached
TRAIL_HEADING = 'trail-heading'


def get_page(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log.error(f'Error during request to {url}: {str(e)}')
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > -1

def get_statuses():
    raw = get_page("https://www.theforks.com/events/skating-trail-and-park-conditions") 
    html = BeautifulSoup(raw, 'html.parser')

    # Use the class of the <svg> element inside each <li> to determine status
    statuses = []
    for item in html.select('li'):
        location = item.text

        status = item.findChildren('svg', recursive=False)
        if status:
            status = status[0]

        # Skip if <li> isn't a location status
        if not status or not location or location in IGNORE:
            continue
        if item.has_attr('class') and TRAIL_HEADING in item['class']:
            continue

        if status.has_attr('class'):
            is_open = None
            classes = status['class']

            if OPEN in classes:
                log.debug(f'{location}: open')
                is_open = 'open'
            elif CONDITIONS_VARIABLE in classes:
                log.debug(f'{location}: conditions variable')
                is_open = 'conditions variable'
            elif CLOSED in classes:
                log.debug(f'{location}: closed')
                is_open = 'closed'
            else:
                log.error(f'ERROR: location - {location}, classes - {classes}')
        
            statuses.append((location, is_open))
    
    return statuses

