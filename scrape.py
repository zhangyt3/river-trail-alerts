from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from pprint import pprint


def get_page(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


# Filter out <li> elements with this text inside during parsing
BLACKLIST = set([
    'Open',
    'Closed',
    'Conditions Variable'
])

# The <svg> elements on the page have these classes when a location is open/closed/maybe
OPEN = 'check'
CLOSED = 'closed'
CONDITIONS_VARIABLE = 'dash'

# <li> elements that are headings have this class attached
TRAIL_HEADING = 'trail-heading'


if __name__ == "__main__":
    raw = get_page("https://www.theforks.com/events/skating-trail-and-park-conditions")
    html = BeautifulSoup(raw, "html.parser")

    # Each <li> element contains a <svg> which displays either a check or an X and some text that
    # tells us the location
    for item in html.select("li"):
        location = item.text

        status = item.findChildren("svg", recursive=False)
        if status:
            status = status[0]

        # Skip if the <li> doesn't correspond to a location status
        if not status or not location or location in BLACKLIST:
            continue
        if item.has_attr('class') and TRAIL_HEADING in item['class']:
            continue

        # Figure out the status based on the class associated with the <svg> element
        if status.has_attr('class'):
            if OPEN in status['class']:
                print(f"{location} is open")
            elif CONDITIONS_VARIABLE in status['class']:
                print(f"{location} is variable")
            elif CLOSED in status['class']:
                print(f"{location} is closed")
            else:
                print("*" * 20)
                print("Opps")
                pprint(status)
                pprint(location)
                print("*" * 20)

